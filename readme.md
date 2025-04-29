# Задача 1. Greedy Decoding
1) Генерация текста не меняется от запуска к запуску
2) В случае генерации сказки результат детерминирован и отсутствует вариативность, так что в случае неудачной генерации придется менять промпт. Текст имеет резкий переход и не содержит деталей. В случае с JSON, он сгенерировался неправильно, и из-за детерминированности на это не повлиять.

3) Текст про ежика и JSON находится в exp1_out/. 

## Пример:

{"contractor": "Mike", "sum": 105, "currency": "rubles"}

Once upon a time, in a small, cozy village nestled in the heart of the forest, there lived a tiny hedgehog named Sonic. Sonic was a curious and adventurous creature, always eager to explore the world around him. One day, while wandering through the forest, Sonic stumbled upon a hidden cave.

As Sonic explored the cave, he discovered a treasure chest filled with magical items. The chest was guarded by a wise old owl who had been watching over the cave for years. The owl, intrigued by Sonic's curiosity, offered to share his knowledge with him.

Sonic listened intently as the owl explained the secrets of the forest and the world around him. He learned about the creatures that lived there, the plants and animals that thrived in the forest, and the magic that was hidden within the cave.

Over the next few days, Sonic spent his days exploring the cave, discovering new treasures and learning more about the world around him. He became a legend in the village, known for his wisdom and his love of adventure.

Years later, Sonic's story would be told to generations of villagers, and the cave would be known as the "Hedgehog's Treasure Cave." Sonic's adventures and his knowledge of the forest would be passed down through the generations, inspiring others to explore the world around them and to seek out the magic that was hidden within the cave.<|im_end|>


# Задача 2. Sampling

1) Генерация различается от запуска к запуску.
2) Генерация не контролируется, и каждый раз получается разный результат. Для задачи с JSON, где ответ определяется примерно однозначно, это плохо (в данном случае ни один сгенерированный JSON не правилен). В сказках про ежика часто отсутствует какой-либо сюжет и присутствуют противоречия/резкие смены обстановки/артефакты.

3) Тексты про ежика и JSON находится в exp2_out/.
 
## Пример:

{"contractor": "Mike Cashier", "sum": "105.05", "currency": "rub"}

Once upon a time, in a small, cozy hedgehog village nestled in the heart of a lush forest, there lived a tiny hedgehog named Sonic. Sonic was not just any hedgehog; he was the tallest and most beautiful, with two bright red eyes and four white paws.

Sonic's village was tucked away in a secluded hill above the forest floor, a place steeped in the unique charm of nature. The villagers loved him for his intelligence, beauty, and unique way of thinking. At the height of the day, their great-great-great grandparents would head for the village in their golden carriages adorned with ribbons and their families would greet him with curious surprise.

Dinner hours were a different story entirely. The village was nestled among other hedges, surrounded by vast gardens filled with flowers, mysterious bugs, and adorned with delicate vines. Genteels and ghosts would join with Sonic and his friends at bedtime, making the village a veritable cultural center of spirits and hermits.

However, it wasn't always so bountiful. Once, an old, eccentric gnoll attacked their village for months and threatened to eat everyone. Only fledgling tangy acorns and their simple habits managed to save the village from unprovoked slaughter. But soon the gnoll would be found, its massive beak beading with precious mithrills.

But Sonic never let the gnoll's tiny _feline_ claws or feline countersing get him down. With his nose to the ground and his open white face, he would feast until his paws stumbled from the grotto, a contented ripple of laughter distancing all in the faintly dot fields of minced meat.

And sometimes, being a tiny hedgehog, Sonic caught small waves through the ocean of the dense forest some nights, offering wistful speeches in his soft, melodious murmur. It was a blissful cover-up to the poignant events of their little town, quite literally, full-of truths.

That was the story of Sonic the Hedgehog. From his quaint village in a secluded tree to the unending adventure into extreme situations, Little Sonic was a charming, happy hedgehog who lived each day being the best he could be, the smartest, and most _blissful ._



# Задача 3. Sampling meets Temperature

1) Тексты сгенерированные с температурой 0.001 почти не отличаются от текстов, сгенерированных в задаче Greedy Decoding. При t=0.1 результат отличается, а при большем увеличении температуры текст становится длиннее и менее связным. При очень большой температуре генерируются околослучайные символы не несущие никакого смысла.
В случае с JSON, лучше использовать более низкую температуру для более одинаковой генерации. Для задачи генерации сказки лучше взять температуру побольше для более разнообразной генерации.

2) Тексты про ежика и JSON находится в exp3_out/. 

## Пример (t=0.1):

{"contractor": "Mike", "sum": 105, "currency": "rubles"}

Once upon a time, in a small, cozy village nestled in the heart of the forest, there lived a tiny hedgehog named Sonic. Sonic was a curious and adventurous creature, always eager to explore the world around him. One day, while wandering through the forest, Sonic stumbled upon a hidden cave.

As Sonic explored the cave, he discovered a treasure chest filled with magical items. The chest was wrapped in a soft, golden blanket, and inside, he found a small, glowing orb. Sonic was thrilled to find this treasure, but he knew that he needed to use it wisely.

With a heavy heart, Sonic decided to use the orb to help the villagers. He used the energy from the orb to create a magical shield that protected the village from the dangers of the forest. The villagers were amazed by Sonic's bravery and the magic he had created.

From that day on, Sonic became a hero in the village. He used his newfound powers to help the people in need, and the villagers were grateful for his kindness. Sonic's adventures continued, and he became known as the guardian of the forest and the protector of the village.

Years passed, and Sonic grew older, but his love for the forest and the villagers never changed. He continued to use his magic to protect the village and help those in need. And so, Sonic was a legend, a hero who had saved the forest and the villagers from danger.

# Задача 4. Nucleus Sampling

1) Тексты с более высокой температурой и большим top_p длиннее, однако с одинаковым top_p и разными температурами (=0.5 и =1.0) тексты про ежика получились одинаковыми. 

2) В целом, при высокой температуре Nucleus Sampling отсекает точно нерелеватные токены, в то время как при семплировании с температурой есть шанс их генерации. При низкой температуре, наиболее релеватные токены нормируются и имеют бОльшие шансы сгенерироваться.

3) Тексты про ежика и JSON находится в exp4_out/. 

## Пример (t=0.5 и top_p=0.9):

{"contractor": "Mike", "sum": 105, "currency": "rubles"}

Once upon a time, in a small, cozy village nestled in the heart of the forest, there lived a tiny hedgehog named Sonic. Sonic was a curious and adventurous creature, always eager to explore the world around him. One day, while wandering through the forest, Sonic stumbled upon a mysterious old oak tree.

The tree was said to hold secrets and mysteries, and Sonic was intrigued. He climbed up to the top of the tree and looked down at the forest below. To his surprise, he saw a group of creatures gathered around a sparkling crystal, which was said to be the key to unlocking the secrets of the forest.

With a determined heart, Sonic decided to explore the crystal and uncover its secrets. He climbed up the tree, and as he reached the top, he saw a group of creatures gathered around a glowing orb. Sonic knew that he had to be careful, but he was determined to see what lay hidden beneath the surface.

As he explored the crystal and orb, Sonic discovered that the forest was not just a place of beauty and wonder, but also a place of danger and mystery. He encountered a group of creatures who were trying to protect the crystal and the orb, but they were not willing to let them go.

In a heart-pounding moment, Sonic used his sharp claws to attack the creatures, and he managed to defeat them. He then used his newfound knowledge of the forest to guide the creatures back to safety, and they were able to retrieve the crystal and the orb.

With the help of the forest creatures, Sonic returned to the village and shared his discovery with the villagers. They were amazed by his bravery and his ability to solve a mystery, and they were grateful for his help.

From that day on, Sonic became known as the hero of the village, and he continued to explore the forest and uncover its secrets, always with a smile on his face. And so, the story of Sonic the Hedgehog lived on, a legend that would forever be remembered.

# Задача 5. Early-Stopped Beam Search

1) Генерация с num_beams=1, length_penalty=1.0 такая же, как и в Greedy Decoding. При num_beams=4, length_penalty=1.0 текст получился более связным и коротким, при меньшем length_penalty (0.5 вместо 1.0 или 2.0) и таком же num_beams приоритет отдался более короткому тексту, который отличается лишь последним предложением. При num_beams=8 текст стал длиннее и содержит более "закрученный" сюжет.

JSON файл везде получился примерно одинаковый и неправильный, однако среди кандидатов были правильные варианты (возможно, здесь можно добавить семплирование по кандидатам?). 

2) В отличие от генерации с Greedy Decoding текст получился более связным и полноценным.
По сравнению с nucleus sampling генерация с beam search более детерминирована и может быть использована задач требующих точный ответ, таких как генерация кода.

3) Тексты про ежика и JSON находится в exp5_out/. 

## Пример (num_beams=4, length_penalty=2.0):

{"contractor": "Mike", "sum": 105, "currency": "RUB"}

Once upon a time, in a small village nestled in the heart of the forest, there lived a tiny hedgehog named Sonic. Sonic was a curious and adventurous creature, always eager to explore the world around him. One day, while wandering through the forest, Sonic stumbled upon a hidden cave.

Inside the cave, Sonic discovered a treasure chest filled with rare and valuable items. As he opened the chest, he realized that the treasure was not just any treasure - it was a gift from a wise old owl who had been watching over the village for generations.

With a heavy heart, Sonic decided to return to the village and share the treasure with its inhabitants. As he walked back through the forest, Sonic couldn't help but feel a sense of gratitude for the gift he had received.

From that day on, Sonic became known as the treasure hunter of the village. He would spend hours exploring the forest, searching for hidden treasures, and sharing them with the people of the village. Sonic's story became a legend, and people from all over the village would come to listen to his tales of adventure and discovery.

And so, Sonic lived happily ever after, forever grateful for the treasure he had found and the people who had given it to him.