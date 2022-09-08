module.exports = {
    outputDir: '../ask_me/dist',
    assetsDir: 'static',
    indexPath: 'index.html',
    devServer: {
        proxy: 'http://localhost:5000'
    },
}