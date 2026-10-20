"""Static site generator for the JANETO.NG recreation.

Run:  python src/build.py
Output goes to ../public_html (upload that folder's contents to DirectAdmin public_html).
No dependencies beyond the Python 3 standard library.
"""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public_html"

SITE = "JANETO.NG"
EMAIL = "ovationsglam@gmail.com"
DESCRIPTION = ("JANETO.NG - Behinde the name. A glimpse into my story, values, "
               "and the journey that makes me who I am.")

# (slug, menu label, <title> label)
PAGES = [
    ("", "Home", None),
    ("about", "About", "About"),
    ("the-me", "THE ME", "THE ME"),
    ("profession", "Profession", "Profession"),
    ("affiliation", "Affiliation", "Affiliation"),
    ("conect-with-me", "Conect with me", "Conect with me"),
    ("schedule-booking-1", "Schedule Booking", "Schedule Booking"),
]


def ico(name, extra=""):
    return f'<i class="ico ico-{name}{(" " + extra) if extra else ""}" aria-hidden="true"></i>'


# --------------------------------------------------------------------------- sections

def sec_hero(p):
    return f'''
<section id="section-169" class="mod mod-hero">
  <div class="aos-wrap" data-aos="fade-up">
    <div class="hero-container">
      <div class="hero-image photo-fit"><div class="photo-blur" style="background-image:url({p}assets/img/janet/brown-beaded-suit.jpg)"></div><div class="photo-full" style="background-image:url({p}assets/img/janet/brown-beaded-suit.jpg)"></div></div>
      <div class="hero-box">
        <div data-aos="slide-up"><h1 class="hd1" style="--fs:45">Meet Me-<br>&nbsp;Janet O.Oyeaalume</h1></div>
        <div class="hsep"></div>
        <div data-aos="slide-up"><h2 class="hd2" style="--fs:25">Behinde the name. <br>A glimpse into my story, values, and the journey that makes me who I am.&nbsp;</h2></div>
      </div>
    </div>
  </div>
</section>'''


def sec_about(p, inner=False):
    return f'''
<section id="section-6aaf158084542" class="mod mod-about{' bg-primary' if inner else ''}">
  <div class="container" data-aos="fade-up">
    <div class="about-row">
      <div class="about-img"><div class="about-image photo-fit" role="img" aria-label="I Am Jane"><div class="photo-blur" style="background-image:url({p}assets/img/janet/curls-portrait.jpg)"></div><div class="photo-full" style="background-image:url({p}assets/img/janet/curls-portrait.jpg)"></div></div></div>
      <div class="about-text">
        <div data-aos="fade-up"><div class="hd1" style="--fs:63">I Am Jane</div></div>
        <div class="hsep"></div>
        <div data-aos="fade-up"><div class="hd2" style="--fs:25">Unapologetically multifaceted.<br>My identity, mindset, and the essence of the woman I am becoming.<br><br></div></div>
      </div>
    </div>
  </div>
</section>'''


# Picture shown in the top-right corner of each THE ME card (same order as TESTIMONIALS),
# from assets/img/the-me/. ("", "") = no picture for that card.
THE_ME_PICS = [
    ("panther", ""), ("ivory", ""), ("spring", ""), ("ocean-water", ""), ("cannapie", ""), ("ruby-gem", ""),
    ("wild-emotions", ""), ("water-drop-sunrise", ""), ("scorpio", ""),
    ("", ""),
    ("", ""), ("italy", ""), ("vanilla", ""),
    ("", ""),
    ("exquisite-luxury-suit", ""), ("candles-lotus", ""),
    ("", ""), ("pearl", ""), ("gold", ""),
]

TESTIMONIALS = [
    ("Jane 1", "As Animal", "Panther", "black-suit-cane"),
    ("Jane 2", "As Colour", "Ivory", "ivory-suit-seated"),
    ("Jane 3", "As Season", "Spring", "white-peplum-sofa"),
    ("Jane 4", "As Element", "Ocean Water", "white-shirt-denim"),
    ("Jane 5", "As Food", "Cannapie", "brown-beaded-suit"),
    ("Jane 6", "As Mineral", "Ruby", "red-blazer-staircase"),
    ("Jane 7", "As Weather", "Wild Emotions", "fur-portrait"),
    ("Jane 8", "As Feeling", "Peaceful", "curls-portrait"),
    ("Jane 9", "As Zodiac Sign", "Scorpio", "black-suit-fur-chair"),
    ("Jane 10", "As Flower", "Orchid", "white-top-palazzo"),
    ("Jane 11", "As Song", "All That Matters in the End", "black-lace-jumpsuit"),
    ("Jane 12", "As Country", "Italy", "red-blazer-staircase"),
    ("Jane 13", "As Scent", "Vanilla", "office-ivory-suit"),
    ("Jane 14", "As Person", "Audrey Hepburn", "black-blazer-dress"),
    ("Jane 15", "As Style", "Exquisite Luxury", "office-black-blazer"),
    ("Jane 16", "As Mood", "Goddess", "champagne-satin-evening"),
    ("Jane 17", "As Dressing", "Flamboyant Corporate", "brown-beaded-suit"),
    ("Jane 18", "As Treasure", "Pearl", "pearls-headshot"),
    ("Jane 19", "As Metals", "Gold", "office-ivory-suit"),
]


def module_title(title, slogan=None, sid=""):
    s = f'\n          <h4 class="mod-slogan">{slogan}</h4>' if slogan else ""
    return f'''
  <div class="container mod-title" data-aos="fade-up">
          <h2 class="mod-header" id="{sid}-title">{title}</h2>
          <hr class="small">{s}
  </div>'''


def sec_theme(p, inner=False):
    items = []
    for i, (label, name, value, img) in enumerate(TESTIMONIALS):
        stars = "".join(ico("star") for _ in range(5))
        items.append(f'''
          <div class="t-item{' active' if i == 0 else ''}">
            <blockquote><div class="t-card">
              <div class="t-image photo-fit" role="img" aria-label="{escape(label)}"><div class="photo-blur" style="background-image:url({p}assets/img/janet/{img}.jpg)"></div><div class="photo-full" style="background-image:url({p}assets/img/janet/{img}.jpg)"></div></div>
              <div class="t-statement{' has-pic' if THE_ME_PICS[i][0] else ''}">
                {f'<div class="t-pic"><img src="{p}assets/img/the-me/{THE_ME_PICS[i][0]}.jpg" alt="{escape(value)}" title="{escape(THE_ME_PICS[i][1] or value)}" loading="lazy"></div>' if THE_ME_PICS[i][0] else ''}
                <div class="t-text">
                <div class="t-wrap"><span class="t-title">{escape(label)}</span><div class="t-name"><h4>{escape(name)}</h4></div></div>
                <p class="lead">{escape(value)}</p>
                <div class="rating">{stars}</div>
                </div>
              </div>
            </div></blockquote>
          </div>''')
    slogan = ("MY WORLD\nBeyond the titles.\n"
              "A little more about my lifestyle, inspirations, and the woman beyond the brand.")
    return f'''
<section id="section-6aaf15893ee7f" class="mod mod-theme bg-primary">{module_title("THE ME", slogan, "section-6aaf15893ee7f")}
  <div class="container" data-aos="fade-up">
    <div class="t-carousel" data-interval="10000">
      <div class="t-inner">{"".join(items)}
      </div>
      <button type="button" class="t-control left" aria-label="Previous"><span class="t-chevron">{ico("chevron-left")}</span></button>
      <button type="button" class="t-control right" aria-label="Next"><span class="t-chevron">{ico("chevron-right")}</span></button>
    </div>
  </div>
</section>'''


def headers_box(sid, title, body, p, box_class, photo, focus):
    return f'''
<section id="{sid}" class="mod mod-split {box_class}">
  <div class="split-img"><img class="split-image" data-parallax="0.5" src="{p}assets/img/{photo}.jpg" style="object-position:{focus}" alt="" loading="lazy"></div>
  <div class="split-container" data-aos="fade-up">
    <div class="split-box">
      <div data-aos="fade-up"><div class="hd1" style="--fs:45">{title}</div></div>
      <div class="hsep"></div>
      <div data-aos="fade-up"><div class="hd2" style="--fs:25">{body}</div></div>
    </div>
  </div>
</section>'''


def sec_practices(p):
    body = ("An Ideas into impact.<br>Discover what I create, offer, and bring to life.<br><br>"
            "&nbsp;MY PROFESSION<br>Trained. Skilled. Experienced.<br>A showcase of my expertise,<br>"
            "qualifications, and professional journey.<br><br>6. MY PASSION<br>Driven by what moves me.<br>"
            "The interests, purpose, and dreams that fuel my journey.7.<br><br>&nbsp;WORK WITH ME<br>"
            "Together, we create extraordinary.<br>Let&rsquo;s connect, collaborate, and turn possibilities into reality.8.<br><br>"
            "MY CLIENTS<br>People. Events. Possibilities.<br>Discover who I serve and the value I bring to every engagement.<br><br>"
            "MY WORK &amp; ACHIEVEMENTS<br>My journey, in milestones.<br>"
            "A glimpse into my projects, accomplishments, and proudest moments.<br><br>")
    return headers_box("section-6aaf1582b193a", "&nbsp;Practices", body, p, "box-tinted", "ropes", "center center")


def sec_ventures(p):
    body = ("<br>Behind | Ovation&rsquo;s Glam Limited  &bull; Training School &bull; Event Management<br>"
            "Catering Services &bull; Interior Decorations<br>&nbsp;AT 🌐 Website: www.ovationsglam.com <br>"
            "📧 Email: info@ovationsglam.com<br>&nbsp;Creating Professionals. Delivering Extraordinary Events..<br>"
            "Trained. Skilled. Experienced.<br>A showcase of my expertise, qualifications, and professional job<br>"
            "&#8203;<br><br><br>")
    return headers_box("section-6acf8fe7e893a", "&nbsp;Ventures", body, p, "box-white", "ropes", "center center")


TEAM = [
    ("As A CEO", "FOUNDER", "A visionary leader building brands, creating opportunities, and turning ideas into impactful ventures.", "office-black-blazer", "center 22%"),
    ("As An EVENTIST", "CREATIVE", "An event professional transforming visions into extraordinary experiences with elegance, precision, and creativity.", "champagne-satin-evening", "center 15%"),
    ("As A COACH", "MULTI-DISCIPLINARY", "A mentor committed to educating, empowering, and inspiring others to discover their potential and achieve excellence.", "ivory-suit-seated", "center 10%"),
    ("As A CHEF", "HACCP", "A culinary creative blending flavour, artistry, and innovation to create memorable dining experience", "white-top-palazzo", "center 12%"),
    ("As A LUXURILIST", "ENTHUSIAST", "A woman drawn to refined living, exceptional experiences, timeless elegance, and the art of luxury..", "fur-portrait", "center 20%"),
    ("As An ENTREPRENUR", "STRATEGIST", "A strategic thinker and opportunity creator passionate about building businesses, empowering people, and making lasting impact.", "office-ivory-suit", "center 25%"),
    ("As An AVIATOR", "MILTI-TASKER", "A trained aviation professional with a passion for excellence, discipline, service, and exploring new horizons.", "black-blazer-dress", "center 10%"),
]


def sec_profession(p, inner=False):
    cards = "".join(f'''
      <div class="team-col">
        <div class="team-member">
          <div class="team-image photo-fit" role="img" aria-label="{escape(n)}"><div class="photo-blur" style="background-image:url({p}assets/img/janet/{img}.jpg)"></div><div class="photo-full" style="background-image:url({p}assets/img/janet/{img}.jpg)"></div></div>
          <div class="team-details">
            <h4 class="member-name">{escape(n)}</h4>
            <p class="position">{escape(pos)}</p>
            <p class="desc">{escape(d)}</p>
          </div>
        </div>
      </div>''' for n, pos, d, img, focus in TEAM)
    slogan = ("Behind | Ovation’s Glam Limited  • Training School • Event Management\n"
              "Catering Services • Interior Decorations\n"
              " The different roles, talents, and identities that define me.\nAT")
    return f'''
<section id="section-6ab3d41226e7b" class="mod mod-team{' bg-primary' if inner else ''}">{module_title("Profession", slogan, "section-6ab3d41226e7b")}
  <div class="container" data-aos="fade-up">
    <div class="team-row">{cards}
    </div>
  </div>
</section>'''


AFFILIATIONS = [
    ("assev", "ASSEV - Association of Event Vendors Nigeria"),
    ("aeva", "AEVA"),
    ("tushmyhall", "Tushmyhall Wedding Planning & Coordination Online Training Institute"),
    ("waka-link-event", "Waka Link Event"),
    ("otilo-event-market", "Otilo Event Market (OEM)"),
    ("xpose-masterclass", "Xpose Masterclass 6.0 - The Resilient EventPreneur"),
    ("ovations-glam", "Ovation's Glam Limited - Events & Signatures"),
    ("ceo-founder-circle", "CEO & Founder Circle"),
]


def sec_affiliation(p, inner=False):
    # Same behaviour as the original owl-carousel: 5 logos visible, endless loop, advances every 3s.
    logos = "".join(f'<div class="logo-item"><img src="{p}assets/img/affiliations/{f}.jpg" alt="{escape(alt)}" title="{escape(alt)}"></div>'
                    for f, alt in AFFILIATIONS)
    return f'''
<section id="section-6ab64f97d49e6" class="mod mod-affiliation bg-primary">{module_title("Affiliation", None, "section-6ab64f97d49e6")}
  <div class="container" data-aos="fade-up">
    <div class="logo-carousel" data-enabled="true" data-items="5" data-autoplay="3000">
      <div class="logo-track">{logos}</div>
    </div>
  </div>
</section>'''


def sec_contact(p, inner=False):
    title = module_title("Conect with me", None, "section-6aaf15894ff4c") if inner else ""
    return f'''
<section id="section-6aaf15894ff4c" class="mod mod-contact{' inner' if inner else ''}">
  <div class="contact-bg" style="background-image:url({p}assets/img/janet/fur-portrait.jpg)"></div>{title}
  <div class="contact-content" data-aos="fade-up">
    <div class="container">
      <div class="contact-row">
        <div class="contact-details">
          <ul class="list-unstyled"><li>Manhattan, New York, NY, United States</li></ul>
          <ul class="list-unstyled">
            <li><a href="tel:999-7777-000">{ico("phone")}<span dir="ltr">999-7777-000</span></a></li>
            <li><a href="mailto:{EMAIL}">{ico("envelope-o")}{EMAIL}</a></li>
            <li>{ico("clock-o")}Mon-Fri - 08:00-19:00</li>
          </ul>
        </div>
        <form class="contact-form js-mail-form" novalidate data-subject="Website contact form" data-form="section" action="{p}send-mail.php" method="post">
          <div class="form-2col">
            <div class="form-group"><input type="text" name="name" data-label="Name" placeholder="Name" class="form-control" required></div>
            <div class="form-group"><input type="text" name="phone" data-label="Phone" placeholder="Phone" class="form-control" data-phone></div>
          </div>
          <div class="form-group"><input type="text" name="email" data-label="Email" placeholder="Email address" class="form-control" required data-email></div>
          <div class="form-group"><textarea class="form-control" name="message" data-label="Message" placeholder="Message"></textarea></div>
          <div class="hp-field" aria-hidden="true"><input type="text" name="website" tabindex="-1" autocomplete="off"></div>
          <button type="submit" class="btn btn-contact">Contact Us</button>
          <p class="form-note" role="status" hidden></p>
        </form>
      </div>
    </div>
    <div class="contact-map">
      <iframe title="Map: Manhattan, New York, NY, United States" loading="lazy" referrerpolicy="no-referrer-when-downgrade"
        src="https://maps.google.com/maps?q=Manhattan%2C%20New%20York%2C%20NY%2C%20United%20States&amp;z=15&amp;hl=en&amp;output=embed"></iframe>
    </div>
  </div>
</section>'''


def sec_booking(p, inner=False):
    return f'''
<section id="section-6ab6501e7ef5f" class="mod mod-booking bg-primary">{module_title("Schedule Booking", None, "section-6ab6501e7ef5f")}
  <div class="container booking-content" data-aos="fade-up">
    <!-- The original SITE123 booking module renders no services here; online booking needs a backend. -->
  </div>
</section>'''


# --------------------------------------------------------------------------- chrome

def nav_items(p, active):
    out = []
    for slug, label, _ in PAGES:
        href = p + (slug + "/" if slug else "")
        cls = ' class="active"' if slug == active else ""
        out.append(f'<li{cls}><a href="{href}"><span>{escape(label)}</span></a></li>')
    return "".join(out)


def header(p, active, home):
    items = nav_items(p, active)
    brand = f'<a href="{p}" class="brand">{ico("brand", "brand-icon")}<span class="website-name">{SITE}</span></a>'
    return f'''
<nav id="mainNav" class="{'is-home' if home else 'is-inner'}">
  <div class="nav-container">
    {brand}
    <div class="nav-right">
      <ul class="navPages">{items}<li class="nav-more" hidden><a href="#" aria-haspopup="true" aria-expanded="false"><span>More</span> {ico("caret-down")}</a><ul class="nav-dropdown"></ul></li></ul>
      <ul class="navActions">
        <li><a href="#" class="js-open-email" aria-label="Email">{ico("envelope")}</a></li>
        <li><a href="#" class="js-open-client" aria-label="Client zone">{ico("user")}</a></li>
      </ul>
    </div>
  </div>
</nav>
<nav id="mainNavMobile">
  <div class="m-left"><a href="#" class="js-open-menu" aria-label="Open menu">{ico("bars")}</a></div>
  {brand}
  <div class="m-right"><a href="#" class="js-open-email" aria-label="Email">{ico("envelope")}</a></div>
</nav>
<div id="popupMenu" class="popup popup-menu" aria-hidden="true">
  <div class="popup-cover"></div>
  <button type="button" class="popup-close left js-close" aria-label="Close">{ico("times")}</button>
  <div class="popup-content">
    <ul class="popup-nav">{items}</ul>
    <div class="popup-actions">
      <a href="#" class="js-open-email" aria-label="Email">{ico("envelope")}</a>
      <a href="#" class="js-open-client" aria-label="Client zone">{ico("user")}</a>
    </div>
  </div>
</div>
<div id="popupEmail" class="popup popup-email" aria-hidden="true">
  <div class="popup-cover"></div>
  <button type="button" class="popup-close js-close" aria-label="Close">{ico("times")}</button>
  <div class="popup-content">
    <div class="email-box">
      <h3>Contact Us</h3>
      <p>Fill out the form or send a direct email to: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <form class="js-mail-form" novalidate data-subject="Website enquiry" data-form="popup" action="{p}send-mail.php" method="post">
        <div class="form-2col">
          <div class="form-group"><label>Full Name</label><input type="text" name="name" data-label="Full Name" placeholder="Full Name" class="form-control" required></div>
          <div class="form-group"><label>Email address</label><input type="text" name="email" data-label="Email" placeholder="Email address" class="form-control" required data-email></div>
        </div>
        <div class="form-group"><label>Description</label><textarea class="form-control" name="message" data-label="Description" rows="4" placeholder="Description"></textarea></div>
        <div class="hp-field" aria-hidden="true"><input type="text" name="website" tabindex="-1" autocomplete="off"></div>
        <button type="submit" class="btn btn-primary btn-block">Send</button>
        <p class="form-note" role="status" hidden></p>
      </form>
    </div>
  </div>
</div>
<div id="popupClient" class="popup popup-client" aria-hidden="true">
  <div class="popup-cover"></div>
  <button type="button" class="popup-close left js-close" aria-label="Close">{ico("times")}</button>
  <div class="popup-content">
    <div class="client-box">
      <div class="client-head">Please enter your email</div>
      <form class="client-form" novalidate>
        <input type="text" class="form-control" placeholder="example@example.com" required data-email>
        <button type="submit" class="btn btn-primary">Sign in or create an account</button>
        <p class="form-note" role="status" hidden></p>
      </form>
    </div>
  </div>
</div>'''


def footer_more_items(p, active):
    # On phones the original footer shows Home, About, THE ME and a "More" drop-up with the rest.
    out = []
    for slug, label, _ in PAGES[3:]:
        href = p + slug + "/"
        cls = ' class="active"' if slug == active else ""
        out.append(f'<li{cls}><a href="{href}"><span>{escape(label)}</span></a></li>')
    return "".join(out)


def footer(p, active):
    return f'''
<footer class="global_footer">
  <div class="part1">
    <div><ul class="navPages">{nav_items(p, active)}<li class="footer-more"><a href="#" aria-haspopup="true" aria-expanded="false"><span>More</span> {ico("caret-down")}</a><ul class="footer-dropdown">{footer_more_items(p, active)}</ul></li></ul></div>
    <div>Copyright © 2026 All rights reserved - <span>{SITE}</span></div>
  </div>
</footer>'''


def page(title, body, p, active, home, depth_note=""):
    return f'''<!DOCTYPE html>
<html lang="en" class="no-js {'home' if home else 'inner'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(DESCRIPTION)}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(DESCRIPTION)}">
<meta property="og:image" content="{p}assets/img/janet/brown-beaded-suit.jpg">
<meta name="theme-color" content="#070104">
<link rel="icon" type="image/svg+xml" href="{p}assets/icons/favicon.svg">
<link rel="preload" href="{p}assets/fonts/roboto-condensed-latin-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{p}assets/css/fonts.css">
<link rel="stylesheet" href="{p}assets/css/style.css">
</head>
<body>
{header(p, active, home)}
<main id="content">{body}
</main>
{footer(p, active)}
<script src="{p}assets/js/main.js" defer></script>
</body>
</html>
'''


def build():
    # Home page: every module, in the original order.
    p = ""
    home_body = "".join([sec_hero(p), sec_about(p), sec_theme(p), sec_practices(p), sec_ventures(p),
                         sec_profession(p), sec_affiliation(p), sec_contact(p), sec_booking(p)])
    (OUT / "index.html").write_text(
        page(f"{SITE} - Meet Me- Janet O.Oyeaalume", home_body, p, "", True), encoding="utf-8")

    inner = {
        "about": sec_about, "the-me": sec_theme, "profession": sec_profession,
        "affiliation": sec_affiliation, "conect-with-me": sec_contact, "schedule-booking-1": sec_booking,
    }
    for slug, _, tlabel in PAGES[1:]:
        p = "../"
        d = OUT / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(
            page(f"{tlabel} - {SITE}", inner[slug](p, inner=True), p, slug, False), encoding="utf-8")

    # 404 page uses root-absolute paths because it can be served from any URL depth.
    p = "/"
    body404 = f'''
<section class="mod mod-404 bg-primary">
  <div class="container mod-title">
    <h2 class="mod-header">Page not found</h2>
    <hr class="small">
    <h4 class="mod-slogan">The page you are looking for doesn't exist.</h4>
    <p><a class="btn btn-primary" href="/">Back to Home</a></p>
  </div>
</section>'''
    (OUT / "404.html").write_text(page(f"Page not found - {SITE}", body404, p, None, False), encoding="utf-8")
    print("Built", len(PAGES) + 1, "pages into", OUT)


if __name__ == "__main__":
    build()
