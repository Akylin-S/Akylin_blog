module.exports = {
    devServer: {
        proxy: {
            '/api': {
                target: `http://127.0.0.1:8000/api`,
                changeOrigin: true,
                pathRewrite: {
                    '^/api': ''
                }
            }
        }
    },
 configureWebpack: {
        resolve: { extensions: [".ts", ".tsx", ".js", ".json"] },
        module: {
            rules: [
                { test: /\.vue$/, loader: 'vue-loader',
                    options: {
                        loaders: {
                            ts: 'ts-loader',
                            tsx: 'babel-loader!ts-loader',
                        }
                    }
                },
                {
                    test: /\.ts$/,
                    loader: 'ts-loader',
                    options: { appendTsSuffixTo: [/TS\.vue$/] }             },
                {
                    test: /\.tsx$/,
                    loader: 'babel-loader!ts-loader',
                    options: {
                        appendTsxSuffixTo: [/TSX\.vue$/]
                    }
                }
            ]
        }
    }
};