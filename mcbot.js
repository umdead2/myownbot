const http = require('http');
const port = process.env.PORT || 8080;

http.createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/plain' });
  res.end('Bot is running\n');
}).listen(port, () => {
  console.log(`Web server listening on port ${port}`);
});

const mineflayer = require('mineflayer')

const bot = mineflayer.createBot({
  host: 'play.minesteal.xyz',
  username: 'MoneyTalks',
  version: '1.21.1',
  hideErrors: true,
  clientRoot: null, 
})

bot.on('inject_allowed', () => {
  bot.physics.enabled = false 
})

bot.on('messagestr', (message) => {
  console.log(`[CHAT] ${message}`)
})
bot.on('resource_pack', () => {
  bot.acceptResourcePack()
})

bot.on('spawn', () => {
  setTimeout(() => {
    bot.chat('/register renars123 renars123')
    bot.chat('/login renars123')
    setTimeout(() => { bot.physics.enabled = true }, 2000)
  }, 3500)
})

bot.on('kicked', (reason) => {
  const msg = typeof reason === 'string' ? reason : JSON.stringify(reason)
  console.log(`[!] KICKED: ${msg}`)
})

bot.on('error', (err) => console.log('[!] Error:', err.message))
bot.on('end', () => console.log('[-] Socket closed. Restarting...'))