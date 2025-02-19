const { app, BrowserWindow } = require('electron');

function createWindow() {
  // Create a new window
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,  // Allow Node.js integration in the renderer process (your HTML)
    }
  });

  // Load your HTML file
  win.loadFile('index.html');
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
