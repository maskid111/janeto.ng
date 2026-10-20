# JANETO.NG: static recreation

A pure HTML/CSS/JavaScript recreation of https://6aaf157545489.site123.me/ (SITE123).
It needs **no Node.js, PHP or database**, so any Apache host, including HostAfrica DirectAdmin, can serve it.

## Folder structure

```
janeto.ng/
├── public_html/              ← UPLOAD THE CONTENTS OF THIS FOLDER
│   ├── index.html            Home (all 9 sections)
│   ├── about/index.html      /about
│   ├── the-me/index.html     /the-me
│   ├── profession/index.html /profession
│   ├── affiliation/index.html /affiliation
│   ├── conect-with-me/index.html /conect-with-me  (original spelling kept)
│   ├── schedule-booking-1/index.html /schedule-booking-1
│   ├── 404.html              "Page not found" page
│   ├── send-mail.php         contact form mail handler (PHP mail())
│   ├── .htaccess             404 page, caching, compression, no directory listing
│   └── assets/
│       ├── css/style.css     all styles (values measured from the live site)
│       ├── css/fonts.css     self-hosted Roboto Condensed
│       ├── js/main.js        header, menus, popups, carousel, parallax, scroll animations, forms
│       ├── fonts/            Roboto Condensed .woff2 (SIL Open Font License)
│       ├── icons/            original SVG icons + brand mark
│       └── img/              original images
└── src/build.py              generator for the HTML pages (Python 3, standard library only)
```

## Upload to HostAfrica (DirectAdmin Evolution)

1. Log in to DirectAdmin and open **System Info & Files → File Manager**.
2. Go to `domains/<your-domain>/public_html/`. Delete or move the default `index.html` placeholder if one is there.
3. On your computer, open `janeto.ng/public_html/` and zip **its contents** (not the folder itself):
   select everything inside, including the hidden `.htaccess` file, then right-click → *Send to → Compressed (zipped) folder*.
4. In File Manager click **Upload**, upload the zip into `public_html/`, then select it and choose **Extract**.
5. Check that `public_html/index.html`, `public_html/assets/` and `public_html/.htaccess` sit directly inside `public_html`,
   not in a sub-folder. Delete the zip afterwards.
6. Visit `https://your-domain/`, `/about/`, `/the-me/` and so on. `/about` (no slash) redirects to `/about/` automatically.

The site uses relative links, so it also works from a sub-folder. Only the 404 page assumes the site is at the domain root.

## Editing content

The pages are generated. Edit the text in `src/build.py`, then run:

```bash
python src/build.py
```

Styles and scripts live in `public_html/assets/` and can be edited directly.

To preview locally, run `python -m http.server 8123 --directory public_html` and open http://localhost:8123.

## What is reproduced

- All 7 public routes, with the same section order, text, images, colours (#560327, #070104, #200111, #eae2e5), font (Roboto Condensed) and spacing.
  Section heights match the live site to within a few pixels at 1366px and 375px widths.
- Header: transparent over the home hero, solid black elsewhere; shrinks from 100px to 80px on scroll (0.35s).
  Active and hover underline; "More ▾" dropdown when the menu doesn't fit (for example at 1024px).
- Mobile header (under 768px): hamburger, centred logo and envelope. Full-screen menu slides down (0.7s).
- Envelope → "Contact Us" popup; user icon → "Please enter your email" client-zone popup.
- AOS-style reveal animations (fade-up / slide-up, 200ms ease, 120px offset), replaying when you scroll back up, as on the original.
- THE ME carousel: Bootstrap-style slide (0.6s ease-in-out), auto-advances every 10s, pauses on hover, arrows, swipe on touch, equal-height slides.
- Practices / Ventures parallax: same maths as the jarallax library the original uses (type "scroll", speed 0.5, black behind the image). Turned off on phones, as on the original.
- Contact section: blurred background with a 60% dark overlay, details, form and map.
- Footer, including the mobile "More ▴" drop-up.

## Backend features (not functional on static hosting)

| Feature | Original | This version |
|---|---|---|
| Contact form and "Contact Us" popup | Sent through SITE123's servers | Posted to `send-mail.php`, which emails ovationsglam@gmail.com with PHP `mail()`. "Thank you for contacting us." appears only after the server confirms. If PHP or mail() isn't available, the visitor's email app opens with the message pre-filled instead. See **Contact form email** below. |
| Client zone (user icon) | SITE123 member sign-in | The popup UI is reproduced. Submitting shows a note that sign-in needs a server-side account system. |
| Schedule Booking | SITE123 booking module | Only the heading shows, as on the original (it has no services configured). Online booking needs a booking backend or an embedded booking service. |

## Contact form email (send-mail.php)

Both forms post to `send-mail.php`. It:

- needs PHP 7.4 or newer with `mail()` enabled (HostAfrica DirectAdmin plans normally include both)
- emails **ovationsglam@gmail.com**, with the visitor's address as *Reply-To*, so clicking Reply in Gmail answers them
- validates the fields, blocks email-header injection, ignores bots through a hidden honeypot field, only accepts posts from your own domain, and allows 5 messages per visitor every 10 minutes

**Set it up after uploading:**

1. In DirectAdmin go to **E-mail Manager → E-mail Accounts** and create `no-reply@your-domain`. The handler sends from `no-reply@<your domain>` by default; a real mailbox on your domain helps Gmail accept the messages rather than flag them as spoofed.
   To use a different address, set `MAIL_FROM` at the top of `send-mail.php`. To change the recipient, edit `MAIL_TO`.
2. Optional but recommended: in DirectAdmin's DNS settings, make sure the domain has SPF (and ideally DKIM) records. DirectAdmin usually creates them.
3. Test it: open `https://your-domain/conect-with-me/`, send a message, and check that "Thank you for contacting us." appears and the email arrives (check Gmail's spam folder the first time).
   If your email app opens instead, PHP or mail() isn't working on the plan, so ask HostAfrica support to enable PHP mail().

## Differences and substitutions

- **SITE123 branding removed:** the "I built my site for free using SITE123" bottom bar, the "Powered by SITE123 - Website creator" footer line and the SITE123 favicon. The favicon is now the site's own brand mark in #560327.
- **Map:** the original uses SITE123's map iframe (`maps-cdn.cdn-files-a.com`). It is replaced with a standard Google Maps embed of the same address, the only external resource.
- **Photos:** all SITE123 stock and placeholder photos are replaced with Janet's own photos in `assets/img/janet/` (trimmed, resized to 1400px max). Her photos are never cropped: each frame (hero, I Am Jane, THE ME, Profession) shows the whole photo, with a soft blurred copy of it filling the spare space (`.photo-fit` in `style.css`). Change them in `src/build.py`: the hero and About lines, `TESTIMONIALS`, `TEAM`, and `sec_contact`.
- **THE ME pictures:** 15 cards have a trait picture from the site owner in the top-right corner of the white panel (`assets/img/the-me/`, list `THE_ME_PICS` in `src/build.py`). Cards 10 (Orchid), 11 (Song), 14 (Audrey Hepburn) and 17 (Flamboyant Corporate) have none; add a file and its name to `THE_ME_PICS` to give them one.
- **Affiliation logos:** the original showed an empty band (SITE123 sample logos that never loaded). It now shows your 8 affiliations (ASSEV, AEVA, Tushmyhall, Waka Link Event, Otilo Event Market, Xpose Masterclass, Ovation's Glam, CEO & Founder Circle) in the same owl-style carousel: 5 visible on desktop and 3 on phones, endless loop, advancing every 3s, pausing on hover. The files are in `assets/img/affiliations/`, and the list is `AFFILIATIONS` in `src/build.py`.
- **THE ME slide height:** the original sometimes re-measures its slides after images load and stretches them (to about 516px or more, depending on timing). This version uses the height from a fresh page load (269px on desktop).
- **Fonts:** Roboto Condensed is served from `assets/fonts` (the current Google Fonts version) rather than Google's CDN, so text can render 1–2px narrower than on the original.
- **Original typos are kept on purpose** ("Behinde", "Conect", "Intentanal", "MILTI-TASKER", and so on), as are the route names.
