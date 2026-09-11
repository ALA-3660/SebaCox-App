/**
 * GLOBAL BANGLA TYPOGRAPHY STANDARD - CENTRALIZED THEME SYSTEM
 * 
 * Hierarchy:
 * 1. Large Heading -> HIND SILIGURI (Page title, Main section heading, Large important titles)
 * 2. Medium Heading -> BALOO DA 2 (Medium heading, Section title, Card heading, Sub-heading, Button text)
 * 3. Body / Normal Text -> TIRO BANGLA (Body text, Description, Label, Helper text, Form text, Messages, List items)
 */

export const BanglaFonts = {
  largeHeading: 'Hind Siliguri',
  mediumHeading: 'Baloo Da 2',
  body: 'Tiro Bangla',
} as const;

export const banglaTypography = {
  // 1. Hind Siliguri - Large Headings & Main Titles
  largeHeading: {
    hero: 'font-hind font-bold text-2xl md:text-3xl text-slate-900 leading-tight tracking-tight',
    pageTitle: 'font-hind font-bold text-xl md:text-2xl text-teal-900 leading-tight tracking-tight',
    sectionMain: 'font-hind font-bold text-lg md:text-xl text-slate-900 leading-snug',
    dialogTitle: 'font-hind font-bold text-base md:text-lg text-slate-900 leading-snug',
  },

  // 2. Baloo Da 2 - Medium Headings, Cards & Button Prompts
  mediumHeading: {
    sectionTitle: 'font-baloo font-bold text-base md:text-lg text-teal-900 leading-snug',
    cardTitle: 'font-baloo font-semibold text-sm md:text-base text-slate-800 leading-snug',
    subHeading: 'font-baloo font-medium text-xs md:text-sm text-slate-700',
    statHeading: 'font-baloo font-bold text-base text-slate-800',
    tabHeading: 'font-baloo font-bold text-xs md:text-sm',
    badge: 'font-baloo font-bold text-[10px] md:text-xs tracking-wide',
    button: 'font-baloo font-bold text-xs md:text-sm tracking-wide',
  },

  // 3. Tiro Bangla - Body, Labels, Helpers, Forms & Status Messages
  body: {
    lead: 'font-tiro font-normal text-sm md:text-base text-slate-700 leading-relaxed',
    normal: 'font-tiro font-normal text-xs md:text-sm text-slate-600 leading-relaxed',
    small: 'font-tiro font-normal text-[11px] md:text-xs text-slate-500 leading-normal',
    label: 'font-tiro font-medium text-xs text-slate-700 block mb-1',
    helper: 'font-tiro font-normal text-[10px] md:text-[11px] text-slate-500 leading-normal',
    formInput: 'font-tiro font-normal text-xs md:text-sm text-slate-800',
    error: 'font-tiro font-normal text-xs text-rose-600 leading-tight',
    success: 'font-tiro font-normal text-xs text-emerald-700 leading-tight',
    info: 'font-tiro font-normal text-xs text-blue-700 leading-tight',
    listItem: 'font-tiro font-normal text-xs text-slate-700 leading-normal',
    quote: 'font-tiro italic text-xs md:text-sm text-slate-600',
  },
} as const;
