import { createI18n } from 'vue-i18n'
import en from './en.js'
import de from './de.js'

const savedLocale = localStorage.getItem('orbis-locale') || 'en'

export const i18n = createI18n({
  legacy: false,
  locale: savedLocale,
  fallbackLocale: 'en',
  messages: { en, de },
})

export function setLocale(locale) {
  i18n.global.locale.value = locale
  localStorage.setItem('orbis-locale', locale)
  document.documentElement.setAttribute('lang', locale)
}
