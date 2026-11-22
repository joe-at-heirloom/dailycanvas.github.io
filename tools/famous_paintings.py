"""Hand-written data for the /famous-paintings guide (built by build_pages.py).

Targets the search "famous paintings" (Ahrefs US, Nov 2026: 157K/mo, KD 9). The intent is
informational, so each entry gives who, when, where to see it today and why it matters.

Titles, years, media and museums are written here rather than read from the catalog: the
Wikimedia entries in curated_catalog.json carry placeholder media ("Oil on canvas" for frescoes)
and some loose museum names. Each image was checked by eye against the painting it claims to be;
Millais's Ophelia was left out because the catalog's image is Waterhouse's 1894 Ophelia.
"""

# Each section: (heading, intro, [entries]). Entry fields:
#   id: curated_catalog.json id      t: title          y: year
#   m: medium                         at: museum, city  n: note (1-2 factual sentences)
#   wp: matching wallpaper page slug (defaults to art-wallpaper)
SECTIONS = [
    ("The Renaissance, 1430s to 1560s",
     "Oil paint, perspective and the rediscovery of ancient Greece and Rome turned painting into "
     "the art of the age, from Florence and Rome to Bruges and Antwerp.",
     [
         dict(id="wikimedia-Q2476169", t="The Arnolfini Portrait", a="Jan van Eyck", y="1434",
              m="Oil on oak panel", at="National Gallery, London", wp="renaissance-wallpaper",
              n="A merchant and his wife stand in a room in Bruges, above a convex mirror that reflects two more "
                "people in the doorway. Van Eyck signed it on the wall in Latin: Jan van Eyck was here, 1434."),
         dict(id="wikimedia-Q184212", t="Primavera", a="Sandro Botticelli", y="c. 1480",
              m="Tempera on panel", at="Uffizi Galleries, Florence", wp="renaissance-wallpaper",
              n="Venus stands in an orange grove with the Three Graces, Mercury, Flora and a blindfolded Cupid. "
                "Botanists have counted about 190 different flowers in the meadow."),
         dict(id="wikimedia-Q81689", t="The Birth of Venus", a="Sandro Botticelli", y="c. 1485",
              m="Tempera on canvas", at="Uffizi Galleries, Florence", wp="renaissance-wallpaper",
              n="The goddess is blown ashore on a scallop shell by the west wind while a nymph waits with a cloak. "
                "It was one of the first large paintings in Florence of a pagan myth rather than a Christian story."),
         dict(id="wikimedia-Q321303", t="The Garden of Earthly Delights", a="Hieronymus Bosch", y="c. 1490–1510",
              m="Oil on oak panel", at="Museo del Prado, Madrid", wp="renaissance-wallpaper",
              n="A triptych: Eden on the left, a crowded garden of pleasures in the middle and a nightmarish hell "
                "on the right. What it means has been argued over for five centuries."),
         dict(id="wikimedia-Q128910", t="The Last Supper", a="Leonardo da Vinci", y="1495–98",
              m="Tempera and oil on plaster", at="Santa Maria delle Grazie, Milan", wp="renaissance-wallpaper",
              n="The apostles react the moment Jesus says one of them will betray him. Leonardo painted on dry "
                "plaster instead of true fresco, so it began to flake within decades; the latest restoration took 21 years and ended in 1999."),
         dict(id="wikimedia-Q12418", t="Mona Lisa", a="Leonardo da Vinci", y="c. 1503–19",
              m="Oil on poplar panel", at="Louvre, Paris", wp="renaissance-wallpaper",
              n="Most likely Lisa Gherardini, the wife of a Florentine silk merchant; Leonardo kept working on it "
                "for years and never handed it over. Its fame exploded after it was stolen from the Louvre in 1911 and missing for two years."),
         dict(id="wikimedia-Q122953", t="The Creation of Adam", a="Michelangelo", y="c. 1512",
              m="Fresco", at="Sistine Chapel, Vatican City", wp="renaissance-wallpaper",
              n="God reaches toward Adam across a narrow gap, the best-known scene on the Sistine Chapel ceiling "
                "Michelangelo painted from 1508 to 1512. He painted standing on scaffolding, not lying on his back."),
         dict(id="wikimedia-Q175036", t="The School of Athens", a="Raphael", y="1509–11",
              m="Fresco", at="Raphael Rooms, Vatican Museums, Vatican City", wp="renaissance-wallpaper",
              n="Plato, pointing up, and Aristotle, gesturing to the earth, walk through a crowd of ancient thinkers. "
                "Raphael is thought to have given Plato the face of Leonardo, and put himself in at the right edge."),
         dict(id="wikimedia-Q174235", t="The Ambassadors", a="Hans Holbein the Younger", y="1533",
              m="Oil on oak panel", at="National Gallery, London",
              n="Two French envoys pose beside a shelf of globes, instruments and a lute with a broken string. "
                "The smear across the floor is a stretched skull that snaps into shape when you look from the side."),
         dict(id="wikimedia-Q844994", t="Venus of Urbino", a="Titian", y="1538",
              m="Oil on canvas", at="Uffizi Galleries, Florence",
              n="A reclining nude who looks straight at the viewer, painted for the future Duke of Urbino. Its pose "
                "was copied for centuries, most famously by Manet in Olympia."),
         dict(id="wikimedia-Q1477909", t="Hunters in the Snow", a="Pieter Bruegel the Elder", y="1565",
              m="Oil on oak panel", at="Kunsthistorisches Museum, Vienna",
              n="Tired hunters and their dogs come home over a hill above a frozen valley full of skaters. It belongs "
                "to a series of the seasons Bruegel painted in 1565, of which five survive."),
     ]),
    ("Baroque and the Dutch Golden Age, 1600s",
     "Dramatic light, real-looking people and, in the Dutch Republic, quiet everyday scenes painted "
     "for a new market of middle-class buyers.",
     [
         dict(id="wiki-caravaggio-judith-beheading-holofernes", t="Judith Beheading Holofernes", a="Caravaggio",
              y="c. 1599", m="Oil on canvas", at="Palazzo Barberini, Rome",
              n="The biblical heroine cuts the throat of the Assyrian general, caught in a hard, stage-like light. "
                "Its violence and realism were copied all over Europe."),
         dict(id="wikimedia-Q506027", t="The Calling of Saint Matthew", a="Caravaggio", y="1599–1600",
              m="Oil on canvas", at="San Luigi dei Francesi, Rome",
              n="Christ points at the tax collector Matthew in a dim counting room, and a beam of light follows his "
                "hand. It still hangs in the chapel it was painted for."),
         dict(id="wikimedia-Q175907", t="Las Meninas", a="Diego Velázquez", y="1656",
              m="Oil on canvas", at="Museo del Prado, Madrid",
              n="The five-year-old Infanta Margarita with her maids of honor, while Velázquez stands at a huge canvas. "
                "The king and queen appear only as a reflection in the mirror on the back wall."),
         dict(id="wiki-vermeer-the-milkmaid", t="The Milkmaid", a="Johannes Vermeer", y="c. 1658",
              m="Oil on canvas", at="Rijksmuseum, Amsterdam",
              n="A kitchen maid pours milk in a quiet, sunlit corner. Vermeer built the crusty bread out of tiny "
                "dabs of pale paint that catch the light."),
         dict(id="wikimedia-Q81087", t="Girl with a Pearl Earring", a="Johannes Vermeer", y="c. 1665",
              m="Oil on canvas", at="Mauritshuis, The Hague", wp="art-wallpaper",
              n="Not a portrait of a known sitter but a tronie, a Dutch study of a face and costume. The pearl is "
                "a couple of strokes of paint and is probably too large to have been real."),
         dict(id="wikimedia-Q1413716", t="The Return of the Prodigal Son", a="Rembrandt", y="c. 1668",
              m="Oil on canvas", at="State Hermitage Museum, St Petersburg",
              n="A father embraces his ragged, kneeling son from the parable in Luke's Gospel. It is one of the "
                "last large paintings Rembrandt made before his death in 1669."),
     ]),
    ("From Rococo to Romanticism, 1760s to 1850s",
     "Painting swung from aristocratic play to revolution, history and the sublime power of nature.",
     [
         dict(id="wikimedia-Q521816", t="The Swing", a="Jean-Honoré Fragonard", y="c. 1767",
              m="Oil on canvas", at="Wallace Collection, London",
              n="A young woman kicks her slipper into the air while her lover hides in the roses below. It is the "
                "defining image of French Rococo."),
         dict(id="wikimedia-Q5765945", t="Oath of the Horatii", a="Jacques-Louis David", y="1784",
              m="Oil on canvas", at="Louvre, Paris",
              n="Three Roman brothers swear to fight to the death for their city as their father holds up their swords. "
                "Shown at the Paris Salon of 1785, it became the model for Neoclassical painting."),
         dict(id="wikimedia-Q179949", t="The Death of Marat", a="Jacques-Louis David", y="1793",
              m="Oil on canvas", at="Royal Museums of Fine Arts of Belgium, Brussels",
              n="The revolutionary journalist lies murdered in his bath, still holding a letter from his killer, "
                "Charlotte Corday. David, his friend, painted it within months."),
         dict(id="wikimedia-Q386079", t="The Third of May 1808", a="Francisco Goya", y="1814",
              m="Oil on canvas", at="Museo del Prado, Madrid",
              n="French soldiers shoot Spanish civilians after the Madrid uprising, the central man flinging his arms "
                "wide. It is often described as one of the first modern images of war."),
         dict(id="wikimedia-Q321816", t="Wanderer above the Sea of Fog", a="Caspar David Friedrich", y="c. 1818",
              m="Oil on canvas", at="Hamburger Kunsthalle, Hamburg", wp="art-wallpaper",
              n="A man seen from behind stands on a rocky crag above a sea of fog. It became the emblem of German "
                "Romanticism and of standing in awe before nature."),
         dict(id="wikimedia-Q173820", t="The Raft of the Medusa", a="Théodore Géricault", y="1818–19",
              m="Oil on canvas", at="Louvre, Paris",
              n="Survivors of a French navy shipwreck in 1816 wave at a distant ship from a makeshift raft. Géricault "
                "interviewed survivors and studied corpses to get it right."),
         dict(id="wikimedia-Q1065921", t="The Hay Wain", a="John Constable", y="1821",
              m="Oil on canvas", at="National Gallery, London",
              n="A horse-drawn cart crosses the river Stour near Flatford Mill in Suffolk. It won a gold medal at the "
                "Paris Salon of 1824 and inspired a generation of French landscape painters."),
         dict(id="met-45434", t="The Great Wave off Kanagawa", a="Katsushika Hokusai", y="c. 1830–32",
              m="Woodblock print", at="The Metropolitan Museum of Art, New York (one of many impressions)",
              wp="great-wave-wallpaper",
              n="A wave about to break over three boats, with Mount Fuji small in the distance, from the series "
                "Thirty-six Views of Mount Fuji. It was printed thousands of times, so museums around the world own copies."),
         dict(id="wikimedia-Q213049", t="Liberty Leading the People", a="Eugène Delacroix", y="1830",
              m="Oil on canvas", at="Louvre, Paris",
              n="Liberty, bare-breasted and holding the tricolor, leads Parisians over a barricade in the July "
                "Revolution of 1830. She later became a model for Marianne, the symbol of France."),
         dict(id="wikimedia-Q736882", t="The Fighting Temeraire", a="J. M. W. Turner", y="1839",
              m="Oil on canvas", at="National Gallery, London", wp="art-wallpaper",
              n="A steam tug tows a veteran warship from the Battle of Trafalgar up the Thames to be broken up, at "
                "sunset. In 2005 a BBC Radio 4 poll named it Britain's favorite painting."),
         dict(id="met-11417", t="Washington Crossing the Delaware", a="Emanuel Leutze", y="1851",
              m="Oil on canvas", at="The Metropolitan Museum of Art, New York",
              n="George Washington crosses the icy Delaware River on Christmas night, 1776, before the Battle of "
                "Trenton. The canvas is more than 12 feet tall and 21 feet wide."),
     ]),
    ("Realism and Impressionism, 1850s to 1880s",
     "Painters turned to ordinary people and modern Paris, then to light and color caught quickly "
     "out of doors.",
     [
         dict(id="wikimedia-Q849766", t="The Gleaners", a="Jean-François Millet", y="1857",
              m="Oil on canvas", at="Musée d'Orsay, Paris",
              n="Three peasant women pick up the stray stalks left after the harvest. At the Salon of 1857 many "
                "critics read it as a political statement about rural poverty."),
         dict(id="wikimedia-Q15963507", t="Le Déjeuner sur l'herbe", a="Édouard Manet", y="1863",
              m="Oil on canvas", at="Musée d'Orsay, Paris",
              n="A nude woman picnics in a wood with two fully dressed men. Rejected by the official Salon, it was "
                "the scandal of the 1863 Salon des Refusés."),
         dict(id="wikimedia-Q15964818", t="Olympia", a="Édouard Manet", y="1863",
              m="Oil on canvas", at="Musée d'Orsay, Paris",
              n="Manet recast Titian's Venus of Urbino as a Paris courtesan who stares straight back at you. It "
                "caused an uproar at the Salon of 1865."),
         dict(id="wikimedia-Q208230", t="Impression, Sunrise", a="Claude Monet", y="1872",
              m="Oil on canvas", at="Musée Marmottan Monet, Paris", wp="monet-wallpaper",
              n="The port of Le Havre in morning haze. A critic mocked its title after the 1874 exhibition, and "
                "the name Impressionism stuck."),
         dict(id="aic-20684", t="Paris Street; Rainy Day", a="Gustave Caillebotte", y="1877",
              m="Oil on canvas", at="Art Institute of Chicago",
              n="Umbrellas on a wet intersection near the Gare Saint-Lazare, in the wide new streets of "
                "Haussmann's Paris. Caillebotte showed it at the third Impressionist exhibition, in 1877."),
         dict(id="wikimedia-Q432399", t="Luncheon of the Boating Party", a="Pierre-Auguste Renoir", y="1880–81",
              m="Oil on canvas", at="Phillips Collection, Washington, DC",
              n="Renoir's friends linger over lunch on a restaurant balcony on the Seine at Chatou. The young woman "
                "playing with the dog, Aline Charigot, later became his wife."),
         dict(id="wikimedia-Q1535990", t="A Bar at the Folies-Bergère", a="Édouard Manet", y="1882",
              m="Oil on canvas", at="Courtauld Gallery, London",
              n="A barmaid at a Paris music hall faces us, while the mirror behind her shows the crowd and a "
                "reflection that doesn't quite add up. It was Manet's last major painting."),
     ]),
    ("Post-Impressionism and the modern era, 1880s to 1930",
     "Artists pushed color, pattern and feeling past what the eye sees, and opened the way to "
     "modern art.",
     [
         dict(id="aic-27992", t="A Sunday on La Grande Jatte", a="Georges Seurat", y="1884–86",
              m="Oil on canvas", at="Art Institute of Chicago", wp="art-wallpaper",
              n="Parisians relax on an island in the Seine, built from small dots of pure color, a method later "
                "called pointillism. Seurat spent two years on it and added the painted border later."),
         dict(id="wikimedia-Q152509", t="Sunflowers", a="Vincent van Gogh", y="1888",
              m="Oil on canvas", at="National Gallery, London", wp="van-gogh-wallpaper",
              n="Painted in Arles in August 1888 to decorate the room where Gauguin would stay. Van Gogh painted "
                "several versions; this one has fifteen flowers."),
         dict(id="wikimedia-Q846341", t="Café Terrace at Night", a="Vincent van Gogh", y="1888",
              m="Oil on canvas", at="Kröller-Müller Museum, Otterlo", wp="van-gogh-wallpaper",
              n="A café on the Place du Forum in Arles, his first painting with a starry sky. He wrote that it was "
                "a night painting without black."),
         dict(id="wikimedia-Q316307", t="Self-Portrait with Bandaged Ear", a="Vincent van Gogh", y="1889",
              m="Oil on canvas", at="Courtauld Gallery, London", wp="van-gogh-wallpaper",
              n="Painted in January 1889, weeks after he cut off his ear during a crisis in Arles. A Japanese print "
                "hangs on the wall behind him."),
         dict(id="wikimedia-Q45585", t="The Starry Night", a="Vincent van Gogh", y="1889",
              m="Oil on canvas", at="Museum of Modern Art, New York", wp="van-gogh-wallpaper",
              n="The view from his window at the asylum in Saint-Rémy before sunrise, with an imagined village and "
                "a flame-like cypress. MoMA acquired it in 1941."),
         dict(id="met-435868", t="The Card Players", a="Paul Cézanne", y="1890–92",
              m="Oil on canvas", at="The Metropolitan Museum of Art, New York",
              n="Provençal farmhands absorbed in a game of cards. Cézanne painted five versions; one was reported "
                "to have sold privately in 2011 for about $250 million."),
         dict(id="wikimedia-Q18891156", t="The Scream", a="Edvard Munch", y="1893",
              m="Tempera and crayon on cardboard", at="National Museum, Oslo",
              n="A figure on a road above the Oslo fjord clutches its face under a blood-red sky. Munch made several "
                "versions in paint, pastel and print; this 1893 painting is the best known."),
         dict(id="wikimedia-Q209755", t="The Kiss", a="Gustav Klimt", y="1907–08",
              m="Oil and gold leaf on canvas", at="Belvedere, Vienna", wp="klimt-wallpaper",
              n="Two lovers wrapped in patterned gold robes kneel at the edge of a flowering meadow. The Austrian "
                "state bought it from the 1908 Kunstschau exhibition, where it was first shown."),
         dict(id="wikimedia-Q506379", t="The Dance", a="Henri Matisse", y="1910",
              m="Oil on canvas", at="State Hermitage Museum, St Petersburg",
              n="Five red dancers whirl in a ring on a green hill against a blue sky, painted for the Moscow "
                "collector Sergei Shchukin. MoMA owns an earlier, paler version."),
         dict(id="wikimedia-Q476798", t="The Dream", a="Henri Rousseau", y="1910",
              m="Oil on canvas", at="Museum of Modern Art, New York",
              n="A woman on a sofa in the middle of a moonlit jungle, with lions, birds and a snake charmer. "
                "Rousseau, a self-taught former customs clerk, never left France."),
         dict(id="aic-97933", t="Water Lilies", a="Claude Monet", y="1917–19",
              m="Oil on canvas", at="Art Institute of Chicago", wp="monet-wallpaper",
              n="The pond Monet built at Giverny, painted with no shore or horizon. He painted his water lilies "
                "about 250 times, from the late 1890s until his death in 1926."),
         dict(id="aic-6565", t="American Gothic", a="Grant Wood", y="1930",
              m="Oil on beaverboard", at="Art Institute of Chicago",
              n="A farmer and his daughter stand in front of a house with a Gothic window in Eldon, Iowa. Wood's "
                "sister and his dentist posed for them."),
     ]),
]

INTRO = (
    "The most famous paintings in the world include the Mona Lisa and The Last Supper by Leonardo "
    "da Vinci, The Starry Night by Vincent van Gogh, Girl with a Pearl Earring by Johannes Vermeer, "
    "The Birth of Venus by Sandro Botticelli, The Creation of Adam by Michelangelo, The Scream by "
    "Edvard Munch, The Kiss by Gustav Klimt and The Great Wave off Kanagawa by Hokusai."
)

FAQ = [
    ("What is the most famous painting in the world?",
     "Leonardo da Vinci's Mona Lisa, in the Louvre in Paris, is generally considered the most famous "
     "painting in the world. Close behind are Van Gogh's The Starry Night, Michelangelo's The Creation of "
     "Adam, Leonardo's The Last Supper, Vermeer's Girl with a Pearl Earring, Botticelli's The Birth of "
     "Venus and Munch's The Scream."),
    ("Why is the Mona Lisa so famous?",
     "It combines Leonardo's reputation, a subtle smile and gaze painted with soft, smoky blending, and a "
     "dramatic history. Its fame grew enormously after an Italian handyman stole it from the Louvre in "
     "1911; it was missing for over two years and its empty spot on the wall drew crowds."),
    ("What is the most expensive painting ever sold?",
     "Salvator Mundi, a painting of Christ attributed to Leonardo da Vinci, sold at Christie's in New York "
     "in November 2017 for $450.3 million, the highest price ever paid for a painting at auction."),
    ("Where can I see the most famous paintings?",
     "Many are in a handful of museums: the Louvre in Paris (Mona Lisa, Liberty Leading the People, The "
     "Raft of the Medusa), the Uffizi in Florence (The Birth of Venus, Primavera), the Prado in Madrid "
     "(Las Meninas), the National Gallery in London (Sunflowers, The Arnolfini Portrait), and in New "
     "York the Museum of Modern Art (The Starry Night) and The Metropolitan Museum of Art."),
    ("Can I use these famous paintings as my wallpaper?",
     "Yes. Every painting on this page is old enough to be in the public domain, so you can download it "
     "free as an iPhone or Mac wallpaper with the links under each one. Daily Canvas can also set a "
     "different masterpiece as your wallpaper every morning."),
]
