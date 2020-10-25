import Vue from 'vue'
import VueI18n from 'vue-i18n'
Vue.use(VueI18n)

export default ({
    app,
    store
}) => {
    //  assumes a store/index.js file has been defined and the variable 'locale' is defined on store
    let defaultLang = "pt"
    app.i18n = new VueI18n({
        locale: store.state.locale || defaultLang,
        fallbackLocale: defaultLang,
        messages: {
            'en': require('~/lang/en.json'),
            'pt': require('~/lang/pt.json')
        }
    });
}