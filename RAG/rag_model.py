from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load Hugging Face models
tokenizer = AutoTokenizer.from_pretrained('facebook/bart-large-cnn')
model = AutoModelForSeq2SeqLM.from_pretrained('facebook/bart-large-cnn')

# Load the sentence transformer model
sbert_model = SentenceTransformer('all-MiniLM-L6-v2')

# Dummy knowledge base for the retrieval part (replace with your own database)
knowledge_base = [
    "The rose symbolizes love, passion, and romance, with red roses being the most associated with deep love.",
    "White roses represent purity, innocence, and new beginnings, making them popular in weddings.",
    "Yellow roses symbolize friendship, joy, and warmth but can also indicate jealousy in some cultures.",
    "Pink roses convey admiration, gratitude, and sweetness, often given as a token of appreciation.",
    "Blue roses, which do not naturally exist, symbolize mystery, the unattainable, and the impossible.",
    "The lily symbolizes purity, renewal, and devotion, often associated with funerals and religious ceremonies.",
    "The lotus flower represents spiritual enlightenment, rebirth, and purity, especially in Buddhism and Hinduism.",
    "Sunflowers symbolize happiness, loyalty, and vitality due to their tendency to follow the sun.",
    "Orchids symbolize luxury, beauty, strength, and love, with different colors carrying unique meanings.",
    "Daisies represent innocence, purity, and new beginnings, often associated with childhood and positivity.",
    "Tulips symbolize deep love and elegance, with red tulips representing passionate love.",
    "Purple tulips convey royalty, admiration, and prosperity, while yellow tulips symbolize cheerful thoughts.",
    "Chrysanthemums symbolize longevity, joy, and loyalty, widely used in Asian cultures for funerals.",
    "The poppy represents remembrance and peace, often worn to honor fallen soldiers in many countries.",
    "Lavender symbolizes serenity, grace, and healing, commonly used for relaxation and aromatherapy.",
    "Carnations have different meanings depending on color: red symbolizes admiration, pink represents motherly love, and white conveys pure love.",
    "The peony symbolizes prosperity, good fortune, and romance, often seen in weddings and Chinese culture.",
    "Hydrangeas symbolize gratitude, understanding, and sometimes apology due to their association with heartfelt emotions.",
    "Daffodils represent new beginnings, hope, and renewal, as they are among the first flowers to bloom in spring.",
    "The forget-me-not flower symbolizes remembrance, true love, and lasting connections.",
    "Marigolds symbolize passion, creativity, and mourning in different cultures, especially in Día de los Muertos celebrations.",
    "The camellia represents admiration, perfection, and longing, with pink camellias symbolizing deep desire.",
    "Gardenias symbolize purity, love, and elegance, often used in perfumes and wedding bouquets.",
    "Hibiscus flowers symbolize beauty, femininity, and delicate charm, often associated with tropical climates.",
    "Magnolias represent dignity, perseverance, and nobility, commonly seen in Southern U.S. traditions.",
    "The jasmine flower symbolizes purity, grace, and sensuality, often used in religious and romantic contexts.",
    "The morning glory represents love in vain, fleeting beauty, and the passage of time due to its short-lived blooms.",
    "Bluebells symbolize humility, gratitude, and everlasting love, often found in woodland areas.",
    "The edelweiss flower represents courage, devotion, and rugged beauty, growing in the high Alps.",
    "Holly symbolizes protection, eternal life, and Christmas traditions due to its evergreen nature.",
    "Zinnias symbolize lasting friendship, endurance, and remembrance, often gifted to show support.",
    "Snapdragons represent strength, grace, and deception, with their dragon-like appearance adding to their mystique.",
    "The bleeding heart flower symbolizes deep love, compassion, and unspoken emotions.",
    "Foxgloves represent both admiration and insincerity, with a connection to folklore and magic.",
    "Anemones symbolize anticipation, fragility, and protection against evil in various cultural traditions.",
    "The crocus represents cheerfulness, youthfulness, and the arrival of spring.",
    "Pansies symbolize thoughtfulness, remembrance, and free-spiritedness, often found in literature and poetry.",
    "The verbena flower represents creativity, healing, and enchantment, with historical associations to magic.",
    "Delphiniums symbolize big-heartedness, positivity, and dignity, often used in floral arrangements.",
    "The azalea symbolizes femininity, passion, and temperance, often given as a sign of care and thoughtfulness.",
    "The wisteria flower represents love, devotion, and longevity, especially in East Asian traditions.",
    "The narcissus symbolizes rebirth, self-love, and new opportunities, linked to Greek mythology.",
    "Gladiolus flowers symbolize strength, integrity, and infatuation, often used in victory celebrations.",
    "The passionflower represents faith, spirituality, and sacrifice, with deep religious symbolism.",
    "The yarrow flower symbolizes healing, courage, and protection, used in traditional medicine and folklore.",
    "Roses have been an emblem of love and beauty since ancient times. In Roman mythology, Venus, the goddess of love, was said to have created roses from her blood, linking the flower to passion and romance. In Victorian language of flowers (floriography), roses were used to convey hidden messages between lovers.",
    "White roses, often referred to as the 'bride's flower,' are used in weddings to symbolize the purity and innocence of a new marriage. In Christianity, the white rose represents the Virgin Mary, adding a layer of sacred symbolism.",
    "The yellow rose was originally a symbol of jealousy and betrayal in the Victorian era, but over time, it evolved into a symbol of friendship and joy. It is now commonly given to friends and loved ones to show appreciation and admiration.",
    "Pink roses have long been associated with grace and elegance. In Victorian times, sending pink roses would convey a message of admiration and gratitude. These roses are often chosen for formal occasions or as tokens of respect and appreciation.",
    "Blue roses are a rarity in nature and are often created through genetic modification. Their symbolism revolves around mystery and the unattainable, which is why they are often used in art and literature to represent longing or a desire that cannot be fulfilled.",
    "The lily is one of the oldest cultivated flowers and has deep religious significance. In Christianity, it is associated with the Virgin Mary, symbolizing purity and motherhood. In Greek mythology, the lily was created from Hera's milk, and in some cultures, it represents renewal and rebirth.",
    "The lotus flower is revered in Asian cultures, especially within Buddhism and Hinduism. It grows from the mud but rises above the water to bloom, symbolizing spiritual enlightenment, beauty, and rebirth. It is often used in religious art to represent the journey of the soul from darkness to light.",
    "Sunflowers, known for their vibrant yellow petals and towering height, are often seen as symbols of vitality, adoration, and faith. In Native American cultures, they are associated with the sun and believed to bring good fortune. The sunflower's unique ability to turn toward the sun also represents the pursuit of positivity.",
    "Orchids are considered the epitome of luxury and beauty, particularly in Eastern cultures. In ancient Greece, orchids were associated with virility and masculinity, while in China, they symbolize love, fertility, and refinement. Orchids are often given as gifts to celebrate important life events.",
    "Daisies are commonly associated with simplicity and innocence, and they are often used to express a pure form of love. In Greek mythology, the daisy was linked to the goddess Aphrodite, symbolizing beauty and new beginnings.",
    "Tulips, native to Central Asia, became a symbol of love and beauty in the Ottoman Empire. During the 'Tulip Era' in Turkey, the flower was celebrated in festivals and art. The tulip remains a symbol of enduring love and elegance, especially in the Netherlands, where it is a national icon.",
    "Chrysanthemums have significant cultural importance in Asia, particularly in Japan and China. In Japan, they are associated with the imperial family and symbolize nobility, while in China, they represent longevity and the joys of life. They are also commonly used in autumn festivals.",
    "Poppies have been used for centuries as a symbol of remembrance, particularly for soldiers who have died in war. Their vibrant red color is said to symbolize the blood of fallen soldiers, and they are worn to honor their sacrifice, especially on Remembrance Day in the UK and Veterans Day in the U.S.",
    "Lavender has long been associated with calming and healing properties. In ancient times, it was used in baths and perfumes to relax the body and mind. Today, it remains a popular flower in aromatherapy and is often used in products for relaxation and stress relief.",
    "Carnations, often called the 'flower of the gods,' have different meanings depending on their color. Red carnations represent love, while pink carnations symbolize a mother's love. White carnations represent pure love and a good luck charm in many cultures.",
    "Peonies are particularly significant in Chinese culture, where they are seen as a symbol of wealth, prosperity, and good fortune. In Western culture, peonies are often used to convey romantic feelings, making them a popular flower for weddings and anniversaries.",
    "Hydrangeas are thought to symbolize heartfelt emotions, with different colors representing different meanings. Blue hydrangeas represent apology, while pink ones convey gratitude. The flower’s large, round shape also makes it a symbol of abundance and grace.",
    "Daffodils are among the first flowers to bloom in spring, making them a symbol of renewal, hope, and new beginnings. In some cultures, they represent the start of new adventures or life chapters. They are commonly given to celebrate the arrival of spring or a new phase in life.",
    "Forget-me-nots have been a symbol of eternal love and remembrance for centuries. In German folklore, it is believed that the flower was named when a knight, dying on a riverbank, told his lady to remember him by this small blue flower. It is often given as a token of undying affection.",
    "Marigolds, known for their vibrant orange and yellow hues, are often used in Day of the Dead celebrations in Mexico to honor deceased loved ones. Their strong fragrance is thought to guide the spirits back to the realm of the living during this sacred time.",
    "The camellia, native to Asia, symbolizes elegance and affection. In Japan, it is revered as a symbol of purity, and in the West, it represents admiration and perfection. Camellias are often given as gifts to express romantic interest or admiration for someone’s beauty or accomplishments.",
    "Gardenias are associated with elegance, charm, and beauty. In Hawaiian culture, gardenias are given as a symbol of love and affection, often worn behind the ear as part of a traditional lei. They are also associated with the notion of secret love and romance.",
    "Hibiscus flowers are often used to symbolize delicate beauty and femininity, particularly in tropical cultures. In Hawaii, the hibiscus is the state flower, representing beauty and the spirit of the islands. It is also associated with the goddess of love and fertility.",
    "Magnolias have been celebrated in the Southern United States for their beauty and strength. They symbolize dignity and perseverance, often growing in harsh environments. In Chinese culture, magnolias also represent nobility and a refined elegance.",
    "Jasmine is a delicate and fragrant flower often linked to romantic love and sensuality. In the Middle East and India, jasmine is used in wedding ceremonies to symbolize beauty and love. It is also used in perfumes due to its intoxicating fragrance.",
    "The morning glory, with its fleeting beauty, symbolizes the fragility of life and love that cannot last. It is often associated with time and the passage of seasons. The morning glory’s rapid bloom and fade represent the fleeting nature of youth and beauty.",
    "Bluebells have long been a symbol of humility and gratitude. They are also believed to have mystical powers, with some folklore suggesting they can bring good luck or protect against evil spirits. In the UK, bluebell forests are a cherished sight in the spring.",
    "Edelweiss is a hardy flower found in the high Alps and is associated with courage and love. It became a symbol of resistance and bravery during WWII in the Alps, where it was worn by soldiers as a symbol of national pride and resilience.",
    "Holly is often associated with Christmas, symbolizing protection, eternal life, and good fortune. In ancient cultures, it was believed to ward off evil spirits. Today, holly is used in holiday decorations and is associated with festive cheer and joy.",
    "Zinnias are known for their vibrant colors and are often given to symbolize lasting friendship. They represent endurance and perseverance, making them a fitting flower for expressing support and loyalty to friends and loved ones.",
    "Snapdragons, with their unique shape, are symbolic of strength, grace, and charm. They are also thought to have mystical properties and are associated with good luck and protection. In medieval times, snapdragons were often used in potions and spells.",
    "The bleeding heart is a flower that symbolizes deep, emotional love and heartbreak. Its shape, resembling a heart with drops of blood, makes it an emblem of intense feelings and the fragility of love.",
    "Foxgloves are often linked to both beauty and danger. In folklore, they are associated with fairies and magic, and their scientific name, Digitalis, refers to their poisonous properties. Despite this, they symbolize both love and deception.",
    "Anemones are thought to symbolize protection against evil, with the ancient Greeks believing they were a gift from the gods. They are also associated with anticipation and fragility, making them a fitting symbol for hope and the fleeting nature of life.",
    "The crocus, emerging early in the spring, symbolizes the rebirth and optimism that comes with a new season. Its bright colors are a beacon of hope and joy after the long winter months.",
    "Pansies, with their wide variety of colors, are symbolic of thoughtfulness and remembrance. In literature, they are often portrayed as a flower representing deep contemplation or affection for someone.",
    "The verbena flower, known for its calming and healing properties, has long been used in herbal remedies. It also symbolizes creativity and enchantment, and in folklore, it was used as a protective charm.",
    "Delphiniums symbolize positivity and dignity, and they are often included in bouquets to convey respect and admiration. The tall, spiky flowers are a common feature in cottage gardens and are used to celebrate special occasions.",
    "The azalea represents feminine beauty and elegance, and it is often used in gardens and landscapes to add a touch of grace and color. In Chinese culture, azaleas are also associated with passion and love.",
    "Wisteria is known for its beautiful cascading flowers and is often seen as a symbol of longevity and enduring love. It is frequently found in traditional gardens in Japan, where it is revered for its elegance and fragrance.",
    "Narcissus flowers, named after the Greek mythological figure Narcissus, symbolize self-love and the dangers of vanity. They are also associated with rebirth and new beginnings, often given as gifts to celebrate a fresh start.",
    "Gladiolus, with its bold appearance, symbolizes strength and moral integrity. The gladiolus is also known as the 'sword lily' due to its sword-like shape, representing the warrior spirit.",
    "The passionflower, with its intricate design, represents faith, spirituality, and sacrifice. It is named after the passion of Christ and is used in Christian symbolism to represent the suffering and redemption of Jesus.",
    "Roses have been linked to various mythologies, such as in ancient Greece, where they were associated with Aphrodite, the goddess of love. According to myth, the first rose bloomed when her lover, Adonis, was wounded. The flower also appears in many literary works as a symbol of passionate, eternal love, like in Shakespeare’s *Romeo and Juliet*.",
    "In Christianity, the white rose is often linked with the Virgin Mary, symbolizing her purity and divine motherhood. During the Renaissance, white roses were frequently depicted in religious art, representing the Madonna’s grace and purity, and were commonly used in altars and sacred ceremonies.",
    "The yellow rose’s association with friendship comes from its ability to bring joy and cheer. In the Victorian era, the yellow rose was used to represent a platonic relationship, and sending a yellow rose was seen as an expression of trust and companionship rather than romantic love.",
    "Pink roses have been favored in modern floral arrangements for their soft, gentle appearance and their meanings of gratitude and admiration. In Japan, pink roses symbolize happiness, and in the United States, they are often chosen to convey a sentiment of appreciation or to celebrate a cherished friendship.",
    "Blue roses are often crafted through dyes or genetically altered plants and are used to convey the idea of the 'impossible.' They symbolize the pursuit of an ideal or an unattainable dream, often found in works of art and poetry as metaphors for elusive aspirations.",
    "Lilies, especially white ones, were used in Ancient Greece as offerings to the gods. They have deep associations with the afterlife and are often used at funerals to symbolize the soul’s journey to heaven. In ancient cultures, they were also associated with motherhood and fertility, particularly with the goddess Hera.",
    "The lotus is a significant symbol in Hinduism, Buddhism, and ancient Egyptian culture. In Hinduism, the goddess Lakshmi is often depicted sitting on a lotus, symbolizing prosperity and purity. In Buddhism, the lotus represents the purity of the mind and the potential for enlightenment, as it rises above the murky waters of illusion.",
    "Sunflowers have been revered in ancient civilizations like the Incas and Aztecs, who saw the sunflower as a symbol of the sun and fertility. In modern times, sunflowers are often used in art and design to evoke feelings of positivity, energy, and good fortune, due to their vibrant color and tendency to follow the sun’s movement.",
    "Orchids have been considered exotic and rare flowers, especially by the Victorians, who believed that orchids symbolized strong passions and deep affection. In ancient Greece, the orchid was a symbol of virility, and in Chinese culture, orchids are often associated with refined beauty and nobility.",
    "Daisies, in medieval times, were believed to represent innocence and a fresh start. The flower was used in folk medicine as a remedy for ailments. Their symbolic association with childhood and purity also made them a popular choice for children's gardens and nurseries.",
    "Tulips originated in the Ottoman Empire and were introduced to Europe in the 16th century. Their association with love became even more prominent during the 'Tulip Mania' in the Netherlands, where tulips became a symbol of wealth and status. They are often gifted to express deep, lasting affection in modern floral traditions.",
    "Chrysanthemums were first cultivated in China in the 15th century and were believed to symbolize longevity and vitality. The flower is also an important part of the Japanese culture, where it is used to celebrate the annual Chrysanthemum Festival. In Western cultures, it is often given as a gift during the autumn season to signify friendship and joy.",
    "Poppies have grown in cultural significance, particularly after World War I, when they became a symbol of remembrance for fallen soldiers. The red poppy has been used in ceremonies across the world to honor military personnel. In ancient Greece, poppies were also linked to the god of sleep, Hypnos, symbolizing rest and peace.",
    "Lavender’s soothing scent has made it a staple in aromatherapy and herbal medicine for centuries. Historically, it was used by the ancient Romans in baths for relaxation, and during the Middle Ages, it was believed to have healing properties and was burned as incense to ward off evil spirits.",
    "Carnations were given as a sign of admiration in ancient Greece and Rome, where they were used in wreaths to honor heroes and gods. They are also said to symbolize a mother's love, which is why pink carnations are commonly gifted on Mother's Day to express affection and gratitude.",
    "Peonies have been used in Chinese medicine for centuries due to their believed healing properties. In Chinese culture, they are considered the 'king of flowers' and symbolize wealth, honor, and a happy marriage. They are often incorporated into traditional Chinese art and floral arrangements to bring good fortune.",
    "Hydrangeas were first cultivated in Japan and China and are linked to a variety of meanings based on their color. Blue hydrangeas represent a sincere apology, while pink ones symbolize understanding and gratitude. The flower’s ability to change colors based on soil pH also gives it a unique connection to change and transformation.",
    "Daffodils are among the first flowers to bloom in spring, making them a symbol of new beginnings. In ancient Greece, the daffodil was linked to the myth of Narcissus, and in modern times, it is often used to symbolize hope and renewal, especially in cancer awareness campaigns.",
    "Forget-me-nots are often used in literature and art as symbols of memory and eternal love. In German folklore, they were believed to be flowers that could be used to recall a loved one’s memory, and in the United States, they are given on special occasions to convey that someone will never be forgotten.",
    "Marigolds are used in many parts of the world for religious and cultural festivals. In Mexico, marigolds are believed to guide the spirits of the dead during Día de los Muertos, while in Hinduism, they are used in religious rituals to honor deities and represent auspicious beginnings.",
    "The camellia was particularly cherished in Victorian England, where it symbolized perfection and beauty. It was often featured in art and literature, representing a refined elegance. In Japan, the camellia has been revered for centuries as a symbol of love and devotion, and its petals are often used in tea ceremonies.",
    "Gardenias have a strong cultural presence in the South of the U.S., where they symbolize elegance, beauty, and purity. In Hawaiian culture, gardenias are used in wedding ceremonies as symbols of love and devotion, and their fragrant blooms are often worn in leis to signify the union of two souls.",
    "Hibiscus flowers have deep significance in many tropical cultures, representing femininity and beauty. In Hawaii, the hibiscus is often given as a symbol of hospitality and is also worn by women in their hair as an indicator of their relationship status—on the right side if they are single, and on the left if they are taken.",
    "Magnolias, particularly in Southern America, are often associated with a sense of home and belonging. The tree, with its large fragrant blossoms, is a symbol of dignity and perseverance, and its appearance in gardens is often a statement of nobility and grace.",
    "Jasmine flowers, known for their rich fragrance, are used in many perfumes and oils. In India, they are a symbol of beauty and sensuality, often used in bridal decorations. The flower also represents simplicity and purity in various cultures and is commonly used in religious offerings.",
    "Morning glories are often associated with the fleeting nature of life, due to their brief bloom. In Japanese culture, morning glories are a symbol of the fleeting beauty of youth, and they are a common subject in summer art and poetry. In Western culture, they symbolize love and affection that is intense but short-lived.",
    "Bluebells are often found in forests, symbolizing humility and gratitude. In Britain, bluebells are seen as fairytale flowers, with folklore suggesting that they were used to summon the fairies. They are also associated with spring’s arrival and are believed to bring good fortune to those who find them.",
    "Edelweiss has been romanticized in song and folklore. It symbolizes both love and bravery due to the difficulty of reaching the high-altitude regions where it grows. During WWII, it was used by the Austrian resistance as a symbol of national pride and a reminder of the country’s cultural heritage.",
    "Holly is traditionally used in Christmas decorations, symbolizing the eternal nature of life due to its evergreen nature. Its bright red berries and spiky leaves have been linked to protection against evil spirits in Celtic folklore, and it was often placed around homes during winter solstice rituals.",
    "Zinnias, known for their bright colors and resilience, represent enduring love and affection. In the language of flowers, they are often used to communicate that love will last despite the passage of time. Zinnias are commonly found in gardens, symbolizing the joy and love of life.",
    "Snapdragons, with their unique flower shape, represent strength and grace. They have been part of folklore for centuries and are sometimes used in magic to bring about good fortune. In modern times, they symbolize insincerity or deception in certain contexts, making them a flower of dual meanings.",
    "The bleeding heart flower has long been associated with deep emotional connection and pain. Its distinct shape has made it a symbol of undying love and suffering. In Victorian times, the flower was often used to represent a love that was painful but passionate, or a love lost.",
    "Foxgloves have been associated with both magic and danger. In folklore, they were believed to be a flower of witches and fairies, while in modern herbalism, they are used for medicinal purposes. Their connection with poison has made them a symbol of hidden danger or deceit in some cultures.",
    "Anemones have been symbols of protection and healing in various cultures. In ancient Greece, they were associated with the goddess Aphrodite, who was said to have created the flower after the death of her lover Adonis. Anemones were also thought to bring luck and ward off evil spirits.",
    "Crocuses symbolize spring’s arrival, bringing color and life after the long winter months. Their early bloom is a sign of hope and renewal, and they have been used in both Greek mythology and modern culture as symbols of the return of warmth and prosperity.",
    "Pansies, with their vibrant petals and distinct colors, have been associated with thoughts and contemplation. They symbolize deep affection, particularly when one is thinking of someone or something special. Their name itself comes from the French word 'pensée,' meaning 'thought.'",
    "The verbena flower has a long history as a symbol of healing and protection. In ancient times, it was believed to be a sacred plant used by druids in rituals. Today, it still represents creativity and enchantment, especially in garden settings where it attracts butterflies and birds.",
    "Delphiniums are beloved for their striking height and color, symbolizing positivity, dignity, and grace. The flower’s tall stems and vibrant hues make it a perfect choice for celebrating important milestones, such as anniversaries, graduations, and birthdays.",
    "Azaleas are known for their wide range of colors and their ability to thrive in many different climates. They represent femininity and grace, making them popular in both formal and informal floral arrangements. In Chinese culture, they are also symbols of wealth and good fortune.",
    "Wisteria is often used in classical gardens for its beautiful cascading blooms. In addition to its symbolism of longevity and endurance, wisteria also represents romance and a love that lasts over time. The flower's sweet fragrance and hanging blooms are beloved for their aesthetic beauty.",
    "Narcissus flowers are a reminder of the story of Narcissus in Greek mythology, symbolizing self-love and vanity. However, they also symbolize rebirth and new beginnings. In many cultures, they are associated with the beginning of spring, marking the arrival of brighter days and new growth."
]

# Function to get real embeddings
def get_embeddings(texts):
    return sbert_model.encode(texts, convert_to_numpy=True).astype('float32')

# Generate embeddings from the knowledge base
embeddings = get_embeddings(knowledge_base)

# Get the correct embedding dimension
embedding_dim = embeddings.shape[1]

# Initialize FAISS index
index = faiss.IndexFlatL2(embedding_dim)

# Add embeddings to FAISS
index.add(embeddings)

# Function to retrieve relevant documents from the knowledge base
def retrieve_documents(query):
    query_embedding = get_embeddings([query])
    _, indices = index.search(query_embedding, k=2)  # Retrieve top 3 documents

    # Only return unique and relevant docs
    retrieved_docs = list(set([knowledge_base[i] for i in indices[0] if i < len(knowledge_base)]))
    
    return retrieved_docs

# Function to generate a response using the retrieved documents
def generate_response(query):
    # Retrieve relevant documents
    relevant_docs = retrieve_documents(query)
    
    # If retrieved docs are too short, fetch all matching knowledge base sentences
    if len(relevant_docs) < 2:
        relevant_docs = [doc for doc in knowledge_base if query.lower() in doc.lower()]

    # Combine query with the relevant documents for the generation model
    input_text = query + " " + " ".join(relevant_docs)
    
    # Generate a response using the Hugging Face model
    inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)
    summary = model.generate(**inputs, num_beams=4, max_length=150, early_stopping=True)
    
    # Decode the generated response
    response = tokenizer.decode(summary[0], skip_special_tokens=True)

    print("User Query:", query)  # Debugging line
    print("Generated Response:", response)  # Debugging line
    
    return response
