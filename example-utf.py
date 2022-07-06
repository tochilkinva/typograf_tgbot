# -*- encoding: utf-8 -*-

from RemoteTypograf import RemoteTypograf

rt = RemoteTypograf() # UTF-8

rt.htmlEntities()
rt.br(1)
rt.p(1)
rt.nobr(3)
# result = rt.processText('"Вы все еще кое-как верстаете в "Ворде"? - Тогда мы идем к вам!"')
result = rt.processText('...Когда В. И. Пупкин увидел в газете ("Сермяжная правда" № 45) рубрику Weather Forecast®, он не поверил своим глазам — температуру обещали ±451 °F.')

print(result)
