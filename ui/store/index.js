//store/index.js
export const state = () => ({
    locales: ['en', 'pt'],
    locale: 'pt'
})

export const mutations = {
    SET_LANG(state, locale) {
        if (state.locales.includes(locale)) {
            state.locale = locale
        }
    }
}