const NodePolyfillPlugin = require("node-polyfill-webpack-plugin")
//const FsWebpackPlugin = require('fs-webpack-plugin');

module.exports = {
    plugins: [
        new NodePolyfillPlugin(),
        // new FsWebpackPlugin([{
        //     // Delete folder `build` recursively
        //     type: 'delete',
        //     files: 'build'
        //   }, {
        //     // Delete file `build/index.test.js`
        //     type: 'delete',
        //     files: 'build/index.test.js'
        //   }, {
        //     // Delete file `build/index.test.js`,
        //     type: 'delete',
        //     files: 'index.test.js',
        //     root: path.resolve(__dirname, 'build') // [!] Must be absolute
        //   }, {
        //     // Delete file `build/index.test.js` and folder `build/test`
        //     type: 'delete',
        //     files: [
        //       'index.test.js',
        //       'test'
        //     ],
        //     root: path.resolve(__dirname, 'build')
        //   }, {
        //     // Copy folder `assets` recursively to `build/assets`
        //     type: 'copy',
        //     files: { from: 'assets', to: 'build' }
        //   }, {
        //     // Copy file `assets/image.png` to `build/image.png`
        //     type: 'copy',
        //     files: { from: 'assets/image.png', to: 'build' }
        //   }])
    ],
    externals: [
        'child_process'
    ],
    resolve: {
        fallback: {
            "net": require.resolve("net-browserify")
        }
    }
}