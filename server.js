const { Client, LocalAuth } = require('whatsapp-web.js');
const express = require('express');
const qrcode = require('qrcode-terminal');

process.on('unhandledRejection', (reason) => {
    console.error('Unhandled Rejection:', reason);
});

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: {
        headless: true,
        args: [
            "--no-sandbox",
            "--disable-setuid-sandbox",
            "--disable-dev-shm-usage",
        ]
    }
});

const app = express();
app.use(express.json());

async function startClient(retries = 5) {
    try {
        await client.initialize();
    } catch (err) {
        console.error("Startup failed:", err.message);

        if (retries > 0) {
            console.log("Retrying startup...");
            setTimeout(() => startClient(retries - 1), 5000);
        }
    }
}

let isReady = false;

client.on('qr', qr => {
    qrcode.generate(qr, { small: true });
});

client.on('ready', async () => {
    console.log('WhatsApp ready!');
    isReady = true;

    const myNumber = "31633179600@c.us"; // your number

    await client.sendMessage(myNumber, "🤖 WhatsApp bot is online.");

    const chats = await client.getChats();

    chats.forEach(chat => {
        if (chat.isGroup) {
            console.log(chat.name, chat.id._serialized);
        }
    });
});

client.on('disconnected', async(reason) => {
    console.log('WhatsApp disconnected:', reason);
    isReady = false;

    try {
        await client.destroy(); // clean shutdown
    } catch (e) {
        console.log("Destroy error:", e.message);
    }

    setTimeout(() => {
        console.log("Reinitializing...");
        startClient();
    }, 5000);
});

client.on('auth_failure', msg => {
    console.error('AUTHENTICATION FAILURE', msg);
});

client.on('loading_screen', (percent, message) => {
    console.log('Loading:', percent, message);
});

client.on('authenticated', () => {
    console.log('Authenticated successfully');
});

async function safeSendMessage(group, message, retries = 3) {
    try {
        return await client.sendMessage(group, message);
    } catch (err) {

        if (err.message.includes("detached Frame") && retries > 0) {
            console.log("Retrying send...");
            await new Promise(r => setTimeout(r, 2000));
            return safeSendMessage(group, message, retries - 1);
        }

        throw err;
    }
}

app.post('/send', async (req, res) => {
    if (!isReady) {
        return res.status(503).json({ error: "WhatsApp not ready" });
    }

    try {
        const { group, message } = req.body;

        await safeSendMessage(group, message);

        res.json({ status: "sent" });
    } catch (err) {
        console.error("Send error:", err);

        res.status(500).json({
            status: "error",
            error: err.message
        });
    }
});

startClient();
app.listen(3000);