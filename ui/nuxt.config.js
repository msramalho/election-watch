import colors from 'vuetify/es5/util/colors'
require('dotenv').config()

const routerBase = process.env.DEPLOY_ENV === 'GH_PAGES' ? {
    router: {
        base: '/election-watch/'
    }
} : {}

export default {
    mode: 'spa',
    ...routerBase,
    /*
     ** Headers of the page
     */
    head: {
        // titleTemplate: '%s - ' + process.env.npm_package_name,
        // title: process.env.npm_package_name || '',
        title: "Election Watch",
        meta: [{
                charset: 'utf-8'
            },
            {
                name: 'viewport',
                content: 'width=device-width, initial-scale=1'
            },
            {
                hid: 'description',
                name: 'description',
                content: process.env.npm_package_description || ''
            }, {
                property: 'og:image',
                content: "https://user-images.githubusercontent.com/19508417/97118189-8c869080-1700-11eb-97d6-0d77a7c2ace0.png"
            }, {
                property: 'og:title',
                content: "Election Watch"
            }, {
                property: 'og:description',
                content: process.env.npm_package_description || ''
            }, {
                property: 'og:url',
                content: "https://msramalho.github.io/election-watch"
            }, {
                property: 'og:locale',
                content: "pt"
            }
        ],
        link: [{
            rel: 'icon',
            type: 'image/x-icon',
            href: process.env.DEPLOY_ENV === 'GH_PAGES' ? '/election-watch/favicon.ico' : '/favicon.ico'
        }]
    },
    /*
     ** Customize the progress-bar color
     */
    loading: {
        color: '#fff'
    },
    /*
     ** Global CSS
     */
    css: ['~/assets/main.css'],
    /*
     ** Plugins to load before mounting the App
     */
    plugins: [
        'plugins/i18n.js'
    ],
    /*
     ** Nuxt.js dev-modules
     */
    buildModules: [
        // Doc: https://github.com/nuxt-community/eslint-module
        // '@nuxtjs/eslint-module',
        '@nuxtjs/vuetify',
    ],
    /*
     ** Nuxt.js modules
     */
    modules: [
        // Doc: https://axios.nuxtjs.org/usage
        ['@nuxtjs/axios', {
            // baseURL: "http://35.234.106.142/",
            // baseURL: process.env.DEPLOY_ENV === 'GH_PAGES' ? "https://peaceful-forest-55095.herokuapp.com/http://35.234.106.142/" : "http://localhost:5000/"
            baseURL: process.env.DEPLOY_ENV === 'GH_PAGES' ? "https://election-watch-api.msramalho.xyz" : "http://35.234.106.142/"
            // baseURL: "http://localhost:5000/"
        }],
        'cookie-universal-nuxt',
    ],
    /*
     ** Axios module configuration
     ** See https://axios.nuxtjs.org/options
     */
    axios: {},
    /*
     ** vuetify module configuration
     ** https://github.com/nuxt-community/vuetify-module
     */
    vuetify: {
        customVariables: ['~/assets/variables.scss'],
        theme: {
            dark: false,
            themes: {
                dark: {
                    primary: colors.blue.darken2,
                    accent: colors.grey.darken3,
                    secondary: colors.amber.darken3,
                    info: colors.teal.lighten1,
                    warning: colors.amber.base,
                    error: colors.deepOrange.accent4,
                    success: colors.green.accent3
                }
            }
        }
    },
    /*
     ** Build configuration
     */
    build: {
        /*
         ** You can extend webpack config here
         */
        extend(config, ctx) {}
    }
}