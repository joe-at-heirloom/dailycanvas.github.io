"""Hand-written data for the /art-movements guide (built by build_pages.py).

Targets the search "art movements" (Ahrefs US, Nov 2026: 6.4K/mo, KD 24). Informational intent:
what each movement was, when and where, who led it, how to recognize it, with examples.

Example images come from curated_catalog.json and were each checked by eye. Titles, years and
museums are written here because the catalog's Wikimedia entries are unreliable on those fields;
"at" is left empty where the holding museum isn't certain. Movements after about 1915 are mostly
still in copyright, so Futurism, Dada, Surrealism, Abstract Expressionism and Pop Art are text only.
"""

# Example: (catalog id, title, artist, year, museum or "")
MOVEMENTS = [
    dict(slug="renaissance", name="The Renaissance", dates="c. 1400–1600", where="Italy",
         artists="Masaccio, Sandro Botticelli, Leonardo da Vinci, Michelangelo, Raphael, Titian",
         d="A rebirth of the art and learning of ancient Greece and Rome that began in Florence in the "
           "early 1400s. Painters used linear perspective, anatomy and oil glazes to build convincing space "
           "and lifelike bodies, and the High Renaissance of Leonardo, Michelangelo and Raphael around 1500 "
           "set the standard for European art for centuries.",
         look="Balanced, symmetrical compositions; one-point perspective; idealized figures; classical "
              "architecture and myth alongside Christian subjects.",
         wp="renaissance-wallpaper",
         ex=[("wikimedia-Q81689", "The Birth of Venus", "Sandro Botticelli", "c. 1485", "Uffizi Galleries, Florence"),
             ("wikimedia-Q12418", "Mona Lisa", "Leonardo da Vinci", "c. 1503–19", "Louvre, Paris"),
             ("wikimedia-Q175036", "The School of Athens", "Raphael", "1509–11", "Vatican Museums, Vatican City")]),
    dict(slug="northern-renaissance", name="The Northern Renaissance", dates="c. 1430–1580",
         where="Flanders, the Netherlands and Germany",
         artists="Jan van Eyck, Rogier van der Weyden, Hieronymus Bosch, Albrecht Dürer, Hans Holbein the Younger, Pieter Bruegel the Elder",
         d="North of the Alps, painters perfected oil paint and minute detail. Their pictures are full of "
           "closely observed things, from fabrics and reflections to winter landscapes, and often carry "
           "hidden symbolism.",
         look="Jewel-like detail and texture; deep, glowing color from layered oil glazes; everyday "
              "objects charged with meaning.",
         wp="renaissance-wallpaper",
         ex=[("wikimedia-Q2476169", "The Arnolfini Portrait", "Jan van Eyck", "1434", "National Gallery, London"),
             ("wikimedia-Q174235", "The Ambassadors", "Hans Holbein the Younger", "1533", "National Gallery, London"),
             ("wikimedia-Q1477909", "Hunters in the Snow", "Pieter Bruegel the Elder", "1565", "Kunsthistorisches Museum, Vienna")]),
    dict(slug="mannerism", name="Mannerism", dates="c. 1520–1600", where="Italy, then Spain and northern Europe",
         artists="Pontormo, Parmigianino, Agnolo Bronzino, El Greco",
         d="After the High Renaissance, artists in Florence and Rome deliberately bent its rules. Bodies "
           "grew long and twisted, color turned cool or acidic, and elegance and artifice mattered more "
           "than natural balance.",
         look="Elongated figures and necks; strained poses; crowded or ambiguous space; polished, "
              "aloof court portraits.",
         ex=[("nga-46182", "Monsignor della Casa", "Pontormo", "c. 1541–44", "National Gallery of Art, Washington, DC"),
             ("nga-46106", "Eleonora di Toledo", "Agnolo Bronzino", "c. 1560", "National Gallery of Art, Washington, DC"),
             ("met-436573", "Cardinal Fernando Niño de Guevara", "El Greco", "c. 1600", "The Metropolitan Museum of Art, New York")]),
    dict(slug="baroque", name="Baroque", dates="c. 1600–1750", where="Rome, then Catholic Europe",
         artists="Caravaggio, Artemisia Gentileschi, Peter Paul Rubens, Gian Lorenzo Bernini, Diego Velázquez",
         d="Born in Rome around 1600 and spread by the Catholic Church and royal courts, Baroque art aims "
           "for drama and emotion. Scenes are caught at their most intense moment and lit like a stage.",
         look="Chiaroscuro, sharp light against deep shadow; diagonal, swirling compositions; rich color "
              "and theatrical gesture.",
         ex=[("wiki-caravaggio-judith-beheading-holofernes", "Judith Beheading Holofernes", "Caravaggio", "c. 1599", "Palazzo Barberini, Rome"),
             ("wikimedia-Q506027", "The Calling of Saint Matthew", "Caravaggio", "1599–1600", "San Luigi dei Francesi, Rome"),
             ("wikimedia-Q175907", "Las Meninas", "Diego Velázquez", "1656", "Museo del Prado, Madrid")]),
    dict(slug="dutch-golden-age", name="The Dutch Golden Age", dates="c. 1600–1680", where="The Dutch Republic",
         artists="Rembrandt, Frans Hals, Johannes Vermeer, Jacob van Ruisdael, Jan Steen",
         d="In the newly independent, Protestant Dutch Republic, painters sold to merchants rather than "
           "the church, and specialized in portraits, landscapes, still lifes and everyday interiors. "
           "The best of them made ordinary moments feel timeless.",
         look="Quiet domestic scenes; soft window light; small canvases made for private homes; "
              "brilliant still lifes and wide, low-horizon landscapes.",
         ex=[("wiki-vermeer-the-milkmaid", "The Milkmaid", "Johannes Vermeer", "c. 1658", "Rijksmuseum, Amsterdam"),
             ("wikimedia-Q81087", "Girl with a Pearl Earring", "Johannes Vermeer", "c. 1665", "Mauritshuis, The Hague"),
             ("wikimedia-Q1413716", "The Return of the Prodigal Son", "Rembrandt", "c. 1668", "State Hermitage Museum, St Petersburg")]),
    dict(slug="ukiyo-e", name="Ukiyo-e", dates="c. 1670s–1900", where="Japan",
         artists="Hishikawa Moronobu, Kitagawa Utamaro, Katsushika Hokusai, Utagawa Hiroshige",
         d="Woodblock prints of the \"floating world\" of Edo, now Tokyo: actors, courtesans and, later, "
           "landscapes and travel views. Cheap and mass-produced, they reached Europe in the 1850s and 60s "
           "and deeply influenced the Impressionists and Van Gogh.",
         look="Flat areas of color; strong outlines; bold cropping and unusual viewpoints; rain, snow "
              "and Mount Fuji.",
         wp="great-wave-wallpaper",
         ex=[("met-53689", "The Courtesan Konosumi", "Kitagawa Utamaro", "c. 1793–94", "The Metropolitan Museum of Art, New York"),
             ("met-45434", "The Great Wave off Kanagawa", "Katsushika Hokusai", "c. 1830–32", "The Metropolitan Museum of Art, New York"),
             ("met-55433", "Sudden Shower over Shin-Ōhashi Bridge", "Utagawa Hiroshige", "1857", "The Metropolitan Museum of Art, New York")]),
    dict(slug="rococo", name="Rococo", dates="c. 1720–1780", where="France, then Europe",
         artists="Antoine Watteau, François Boucher, Jean-Honoré Fragonard, Giovanni Battista Tiepolo",
         d="A lighter, playful offshoot of the Baroque that took hold in Paris after the death of Louis XIV "
           "in 1715. Its subjects are love, leisure and flirtation in parks and boudoirs.",
         look="Pastel colors; curving, decorative forms; feathery brushwork; aristocrats at play.",
         ex=[("met-437926", "Mezzetin", "Antoine Watteau", "c. 1718–20", "The Metropolitan Museum of Art, New York"),
             ("met-435739", "The Toilette of Venus", "François Boucher", "1751", "The Metropolitan Museum of Art, New York"),
             ("wikimedia-Q521816", "The Swing", "Jean-Honoré Fragonard", "c. 1767", "Wallace Collection, London")]),
    dict(slug="neoclassicism", name="Neoclassicism", dates="c. 1760–1830", where="France, then Europe and America",
         artists="Jacques-Louis David, Jean-Auguste-Dominique Ingres, Angelica Kauffman, Antonio Canova",
         d="A reaction against Rococo frivolity, inspired by the excavations of Pompeii and Herculaneum and "
           "by Enlightenment ideals. Painters told stories of civic virtue and sacrifice from ancient Rome "
           "in a clean, sober style.",
         look="Crisp outlines and smooth, invisible brushwork; calm, frieze-like compositions; Roman "
              "architecture and costume.",
         ex=[("wikimedia-Q5765945", "Oath of the Horatii", "Jacques-Louis David", "1784", "Louvre, Paris"),
             ("wikimedia-Q179949", "The Death of Marat", "Jacques-Louis David", "1793", "Royal Museums of Fine Arts of Belgium, Brussels"),
             ("aic-111317", "Amédée-David, the Comte de Pastoret", "Jean-Auguste-Dominique Ingres", "1823–26", "Art Institute of Chicago")]),
    dict(slug="romanticism", name="Romanticism", dates="c. 1790–1850", where="Europe",
         artists="Francisco Goya, Caspar David Friedrich, J. M. W. Turner, John Constable, Théodore Géricault, Eugène Delacroix",
         d="Romantic painters put feeling, imagination and the overwhelming power of nature ahead of reason "
           "and rules. Storms, shipwrecks, revolutions and lone figures before vast landscapes are its "
           "subjects.",
         look="Dramatic skies and light; loose, energetic brushwork; the sublime in nature; heroism, "
              "terror and longing.",
         ex=[("wikimedia-Q321816", "Wanderer above the Sea of Fog", "Caspar David Friedrich", "c. 1818", "Hamburger Kunsthalle, Hamburg"),
             ("wikimedia-Q173820", "The Raft of the Medusa", "Théodore Géricault", "1818–19", "Louvre, Paris"),
             ("wikimedia-Q736882", "The Fighting Temeraire", "J. M. W. Turner", "1839", "National Gallery, London")]),
    dict(slug="hudson-river-school", name="The Hudson River School", dates="c. 1825–1875", where="United States",
         artists="Thomas Cole, Asher B. Durand, Frederic Edwin Church, Albert Bierstadt",
         d="America's first homegrown school of painting: large, luminous landscapes of the Hudson Valley "
           "and the Catskills, later of the American West and South America, painted as a celebration of "
           "a wild continent.",
         look="Panoramic views; glowing, golden light; tiny human figures dwarfed by mountains, falls "
              "and sky.",
         ex=[("nga-50727", "A View of the Mountain Pass Called the Notch of the White Mountains", "Thomas Cole", "1839", "National Gallery of Art, Washington, DC"),
             ("aic-76571", "View of Cotopaxi", "Frederic Edwin Church", "1857", "Art Institute of Chicago"),
             ("aic-146701", "Mountain Brook", "Albert Bierstadt", "1863", "Art Institute of Chicago")]),
    dict(slug="realism", name="Realism", dates="c. 1840–1880", where="France, then Europe and America",
         artists="Gustave Courbet, Jean-François Millet, Honoré Daumier, Rosa Bonheur, Winslow Homer",
         d="Realists rejected idealized history and myth to paint ordinary people and the world as it was, "
           "including hard labor and poverty. Gustave Courbet led the movement in France and insisted on "
           "painting only what he could see.",
         look="Peasants, workers and everyday life at full scale; earthy colors; no idealizing or "
              "moralizing gloss.",
         ex=[("met-438820", "Young Ladies of the Village", "Gustave Courbet", "1851–52", "The Metropolitan Museum of Art, New York"),
             ("wikimedia-Q849766", "The Gleaners", "Jean-François Millet", "1857", "Musée d'Orsay, Paris"),
             ("aic-25865", "The Herring Net", "Winslow Homer", "1885", "Art Institute of Chicago")]),
    dict(slug="pre-raphaelites", name="The Pre-Raphaelites", dates="1848–c. 1900", where="England",
         artists="Dante Gabriel Rossetti, John Everett Millais, William Holman Hunt, Edward Burne-Jones",
         d="A brotherhood of young English painters, founded in 1848, who wanted to return to the vivid "
           "color and detail of art before Raphael. Their later work, led by Rossetti and Burne-Jones, "
           "drifted toward dreamy medieval and literary subjects.",
         look="Saturated jewel colors; sharp detail in every leaf; long-haired women; subjects from "
              "Dante, Shakespeare and Arthurian legend.",
         ex=[("met-435826", "The Love Song", "Edward Burne-Jones", "1868–77", "The Metropolitan Museum of Art, New York"),
             ("aic-16551", "Beata Beatrix", "Dante Gabriel Rossetti", "1871–72", "Art Institute of Chicago")]),
    dict(slug="impressionism", name="Impressionism", dates="c. 1867–1886", where="France",
         artists="Claude Monet, Pierre-Auguste Renoir, Edgar Degas, Camille Pissarro, Berthe Morisot, Alfred Sisley, Mary Cassatt",
         d="A group of Paris painters, shut out of the official Salon, held eight exhibitions of their own "
           "from 1874 to 1886. They painted quickly, often outdoors, to catch changing light and modern "
           "life: cafés, boating parties, railway stations and city streets.",
         look="Short, visible brushstrokes; bright, unblended color; colored shadows; everyday modern "
              "subjects and open-air light.",
         wp="monet-wallpaper",
         ex=[("wikimedia-Q208230", "Impression, Sunrise", "Claude Monet", "1872", "Musée Marmottan Monet, Paris"),
             ("aic-11723", "Woman at Her Toilette", "Berthe Morisot", "1875–80", "Art Institute of Chicago"),
             ("wikimedia-Q432399", "Luncheon of the Boating Party", "Pierre-Auguste Renoir", "1880–81", "Phillips Collection, Washington, DC")]),
    dict(slug="symbolism", name="Symbolism", dates="c. 1880–1910", where="France, Belgium and across Europe",
         artists="Gustave Moreau, Odilon Redon, Arnold Böcklin, Fernand Khnopff, Edvard Munch",
         d="Symbolists turned away from the visible world toward dreams, myth, death and the inner life, "
           "using images as symbols of ideas and moods rather than records of things seen.",
         look="Mysterious, often eerie scenes; femmes fatales and sphinxes; twilight and silence.",
         ex=[("met-437153", "Oedipus and the Sphinx", "Gustave Moreau", "1864", "The Metropolitan Museum of Art, New York"),
             ("met-435683", "Island of the Dead", "Arnold Böcklin", "1880", "The Metropolitan Museum of Art, New York"),
             ("wikimedia-Q18891156", "The Scream", "Edvard Munch", "1893", "National Museum, Oslo")]),
    dict(slug="neo-impressionism", name="Neo-Impressionism (pointillism)", dates="c. 1886–1910", where="France",
         artists="Georges Seurat, Paul Signac, Henri-Edmond Cross, Maximilien Luce",
         d="Georges Seurat replaced the Impressionists' instinct with color science, building pictures from "
           "small dots of pure color meant to blend in the viewer's eye. The method is known as pointillism "
           "or divisionism.",
         look="Even dots or dashes of unmixed color; still, carefully composed scenes; shimmering, "
              "luminous surfaces.",
         ex=[("aic-27992", "A Sunday on La Grande Jatte", "Georges Seurat", "1884–86", "Art Institute of Chicago"),
             ("aic-122130", "Les Andelys, Côte d'Aval", "Paul Signac", "1886", "Art Institute of Chicago"),
             ("aic-100476", "Beach at Cabasson", "Henri-Edmond Cross", "1891–92", "Art Institute of Chicago")]),
    dict(slug="post-impressionism", name="Post-Impressionism", dates="c. 1886–1905", where="France",
         artists="Paul Cézanne, Vincent van Gogh, Paul Gauguin, Henri de Toulouse-Lautrec",
         d="Not a single style but the artists who took Impressionism's bright color in personal "
           "directions: Cézanne toward structure, Van Gogh toward emotion, Gauguin toward flat color and "
           "symbol. The English critic Roger Fry coined the name in 1910.",
         look="Bold, expressive color; thick or patterned brushwork; simplified, solid forms; personal "
              "vision over optical accuracy.",
         wp="van-gogh-wallpaper",
         ex=[("wikimedia-Q45585", "The Starry Night", "Vincent van Gogh", "1889", "Museum of Modern Art, New York"),
             ("met-435868", "The Card Players", "Paul Cézanne", "1890–92", "The Metropolitan Museum of Art, New York"),
             ("met-438821", "Ia Orana Maria (Hail Mary)", "Paul Gauguin", "1891", "The Metropolitan Museum of Art, New York")]),
    dict(slug="art-nouveau", name="Art Nouveau and the Vienna Secession", dates="c. 1890–1914",
         where="Paris, Brussels, Vienna and beyond",
         artists="Gustav Klimt, Alphonse Mucha, Koloman Moser, Aubrey Beardsley",
         d="An international decorative style of flowing, plant-like lines that ran from posters and "
           "architecture into painting. In Vienna, Klimt and others broke away from the academy in 1897 to "
           "found the Secession, whose art mixes gold, ornament and symbolism.",
         look="Whiplash curves; flat ornamental patterns; gold leaf; stylized women and flowers.",
         wp="klimt-wallpaper",
         ex=[("wiki-klimt-pallas-athene", "Pallas Athene", "Gustav Klimt", "1898", "Wien Museum, Vienna"),
             ("wikimedia-Q209755", "The Kiss", "Gustav Klimt", "1907–08", "Belvedere, Vienna"),
             ("met-436819", "Mäda Primavesi", "Gustav Klimt", "1912–13", "The Metropolitan Museum of Art, New York")]),
    dict(slug="fauvism", name="Fauvism", dates="c. 1905–1908", where="France",
         artists="Henri Matisse, André Derain, Maurice de Vlaminck, Raoul Dufy",
         d="At the 1905 Salon d'Automne in Paris a critic called Matisse and his friends fauves, \"wild "
           "beasts\", for their violent, unnatural color. Color was set free from describing things and "
           "used for feeling and structure.",
         look="Pure, clashing color straight from the tube; green faces and red trees; loose, "
              "simplified drawing.",
         ex=[("aic-87045", "Still Life with Geranium", "Henri Matisse", "1906", "Art Institute of Chicago"),
             ("smk-KMSr14", "Woman in a Chemise", "André Derain", "1906", "Statens Museum for Kunst, Copenhagen")]),
    dict(slug="expressionism", name="Expressionism", dates="c. 1905–1925", where="Germany and Austria",
         artists="Ernst Ludwig Kirchner, Emil Nolde, Franz Marc, Wassily Kandinsky, Egon Schiele",
         d="Expressionists distorted form and color to convey emotion and anxiety rather than appearance. "
           "Its two main groups were Die Brücke (The Bridge), founded in Dresden in 1905, and Der Blaue "
           "Reiter (The Blue Rider), formed in Munich in 1911.",
         look="Jagged, angular forms; harsh or symbolic color; raw brushwork; city streets, nudes, "
              "animals and spiritual themes.",
         ex=[("cleveland-142792", "Wrestlers in a Circus", "Ernst Ludwig Kirchner", "1909", "Cleveland Museum of Art"),
             ("aic-8980", "Landscape with Two Poplars", "Wassily Kandinsky", "1912", "Art Institute of Chicago"),
             ("aic-9021", "The Bewitched Mill", "Franz Marc", "1913", "Art Institute of Chicago")]),
    dict(slug="cubism", name="Cubism", dates="c. 1907–1920s", where="Paris",
         artists="Pablo Picasso, Georges Braque, Juan Gris, Fernand Léger, Robert Delaunay",
         d="Picasso and Braque broke objects into facets and showed them from several viewpoints at once, "
           "then began gluing paper and newsprint into their pictures. It opened the way to most of the "
           "abstract art that followed. Picasso's and Braque's own works are still under copyright, so "
           "the examples here are by Gris and Léger.",
         look="Fragmented, overlapping planes; muted browns and grays at first, brighter later; guitars, "
              "bottles, newspapers and café tables.",
         ex=[("nga-56101", "Fantômas", "Juan Gris", "1915", "National Gallery of Art, Washington, DC"),
             ("nga-166491", "Glass and Checkerboard", "Juan Gris", "c. 1917", "National Gallery of Art, Washington, DC"),
             ("smk-KMS6627", "Woman with a Vase", "Fernand Léger", "1924", "Statens Museum for Kunst, Copenhagen")]),
    dict(slug="futurism", name="Futurism", dates="1909–c. 1916", where="Italy",
         artists="Umberto Boccioni, Giacomo Balla, Gino Severini, Carlo Carrà",
         d="Launched by the poet F. T. Marinetti's manifesto in 1909, Futurism celebrated speed, machines "
           "and the modern city, and rejected the past. Its painters showed movement as repeated, "
           "overlapping forms.",
         look="Blurred, repeated shapes suggesting motion; lines of force; cars, trains, crowds and "
              "electric light.",
         ex=[]),
    dict(slug="suprematism-and-constructivism", name="Suprematism and Constructivism", dates="c. 1915–1930",
         where="Russia",
         artists="Kazimir Malevich, Lyubov Popova, El Lissitzky, Alexander Rodchenko",
         d="Kazimir Malevich reduced painting to pure geometric shapes, unveiling Black Square in 1915. "
           "After the 1917 revolution, Constructivists such as Popova and Rodchenko turned abstraction "
           "toward design, posters and building a new society.",
         look="Flat geometric forms floating on white; squares, bars and wedges; later, typography and "
              "industrial design.",
         ex=[("wikimedia-Q2364258", "Black Square", "Kazimir Malevich", "1915", "Tretyakov Gallery, Moscow"),
             ("wikimedia-Lyubov-Popova-Painterly-architectonic-1918", "Painterly Architectonic", "Lyubov Popova", "1918", "")]),
    dict(slug="dada", name="Dada", dates="c. 1916–1924", where="Zurich, Berlin, Paris and New York",
         artists="Marcel Duchamp, Hannah Höch, Jean Arp, Kurt Schwitters, Man Ray",
         d="Founded at the Cabaret Voltaire in Zurich in 1916 in disgust at the First World War, Dada "
           "mocked art itself with nonsense, collage, chance and readymades, such as Marcel Duchamp's "
           "urinal, Fountain (1917).",
         look="Collage and photomontage; found objects; absurd titles; deliberate provocation.",
         ex=[]),
    dict(slug="de-stijl", name="De Stijl", dates="1917–1931", where="The Netherlands",
         artists="Piet Mondrian, Theo van Doesburg, Gerrit Rietveld, Bart van der Leck",
         d="A Dutch group named after its magazine, De Stijl (The Style), that reduced art to straight "
           "lines, right angles and the primary colors with black, white and gray. Mondrian called his "
           "version Neo-Plasticism.",
         look="Black grids; flat rectangles of red, yellow and blue; only horizontals and verticals, "
              "until van Doesburg began tilting his grids in the mid-1920s.",
         ex=[("wikimedia-Peinture-pure-1920-Theo-van-Doesburg-Mus-e-national-d-art-moderne", "Pure Painting", "Theo van Doesburg", "1920", "Centre Pompidou, Paris"),
             ("wikimedia-Mondrian-Composition-No-II-with-Red-and-Blue-1929", "Composition No. II, with Red and Blue", "Piet Mondrian", "1929", "")]),
    dict(slug="surrealism", name="Surrealism", dates="c. 1924–1950s", where="Paris, then worldwide",
         artists="Salvador Dalí, René Magritte, Max Ernst, Joan Miró, Leonora Carrington",
         d="Founded in Paris with André Breton's 1924 manifesto, Surrealism tried to unlock the "
           "unconscious through dream imagery, automatic drawing and chance. Its best-known painting is "
           "Salvador Dalí's The Persistence of Memory (1931), with its melting watches.",
         look="Dreamlike, impossible scenes painted with realistic precision; strange juxtapositions; "
              "or loose, automatic doodles and biomorphic shapes.",
         ex=[]),
    dict(slug="abstract-expressionism", name="Abstract Expressionism", dates="c. 1943–1960", where="New York",
         artists="Jackson Pollock, Willem de Kooning, Mark Rothko, Lee Krasner, Barnett Newman",
         d="The first American movement to lead world art, centered in New York after the Second World "
           "War: huge canvases of gestural paint, like Jackson Pollock's drips, or fields of color, like "
           "Mark Rothko's glowing rectangles.",
         look="Wall-sized canvases; drips, splashes and slashing brushwork; or vast, quiet areas of "
              "color.",
         ex=[]),
    dict(slug="pop-art", name="Pop Art", dates="c. 1955–1970", where="Britain and the United States",
         artists="Andy Warhol, Roy Lichtenstein, Richard Hamilton, Claes Oldenburg",
         d="Pop artists borrowed from advertising, comic strips and supermarket shelves, as in Andy "
           "Warhol's Campbell's Soup Cans (1962) and Roy Lichtenstein's blown-up comic panels.",
         look="Bright commercial colors; celebrities and brand names; screen printing, Ben-Day dots and "
              "repetition.",
         ex=[]),
]

INTRO = (
    "An art movement is a style or approach shared by a group of artists at a particular time and "
    "place. The major movements in Western painting, in order, are the Renaissance, Mannerism, Baroque, "
    "Rococo, Neoclassicism, Romanticism, Realism, Impressionism, Post-Impressionism, Symbolism, Art "
    "Nouveau, Fauvism, Expressionism, Cubism, Futurism, Dada, Surrealism, Abstract Expressionism and "
    "Pop Art."
)

FAQ = [
    ("What are the major art movements in order?",
     "In Western painting: the Renaissance (c. 1400–1600), Mannerism (c. 1520–1600), Baroque "
     "(c. 1600–1750), Rococo (c. 1720–1780), Neoclassicism (c. 1760–1830), Romanticism (c. 1790–1850), "
     "Realism (c. 1840–1880), Impressionism (c. 1867–1886), Post-Impressionism (c. 1886–1905), Symbolism "
     "(c. 1880–1910), Art Nouveau (c. 1890–1914), Fauvism (c. 1905–1908), Expressionism (c. 1905–1925), "
     "Cubism (c. 1907–1920s), Futurism (1909–c. 1916), Dada (c. 1916–1924), Surrealism (c. 1924–1950s), "
     "Abstract Expressionism (c. 1943–1960) and Pop Art (c. 1955–1970). The dates overlap, and art "
     "historians draw the edges differently."),
    ("What is the difference between Impressionism and Post-Impressionism?",
     "Impressionists such as Monet and Renoir tried to record a fleeting moment of light and color as "
     "the eye sees it. Post-Impressionists such as Cézanne, Van Gogh and Gauguin kept the bright palette "
     "but used it for structure, emotion or symbolism, moving away from what the eye sees toward a "
     "personal vision."),
    ("What art movement was Van Gogh part of?",
     "Vincent van Gogh is a Post-Impressionist. He absorbed Impressionism and Japanese prints in Paris "
     "in 1886–88, then developed his own style of thick, expressive brushwork and intense color in "
     "Arles and Saint-Rémy. His work strongly influenced Fauvism and Expressionism."),
    ("What is the difference between Baroque and Rococo?",
     "Baroque art (c. 1600–1750) is grand, dramatic and often religious, with deep shadows and strong "
     "emotion. Rococo (c. 1720–1780) grew out of it in France and is lighter and more intimate: pastel "
     "colors, playful curves and scenes of love and leisure for aristocratic homes."),
    ("Why are there no pictures for Surrealism, Abstract Expressionism or Pop Art?",
     "Most works from those movements are still protected by copyright. Every image on this page is in "
     "the public domain, which is also why each one can be downloaded free as a wallpaper."),
]
