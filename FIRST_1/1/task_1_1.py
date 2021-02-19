# duration = 2*3600 + 5*60 + 16  # 2 час 5 мин 16 сек
# duration = 11*2_592_000 + 26*86_400 + 2*3600 + 5*60 + 16  # 11 мес 26 с 2 час 5 мин 16 сек

"""
15 лет + 14 мес. + 35 суток + 28 часов + 63 минуты + 72 сек =
16 год 3 мес 6 с 5 час 4 мин 12 сек
"""
duration = 15*31_104_000 + 14*2_592_000 + 35*86_400 + 28*3600 + 63*60 + 72

sec = duration % 60
minutes = duration // 60 % 60
hours = duration // 3_600 % 3_600 % 24
# я делал задание по пред. версии методички, там пункт d был интереснее, я решил его оставить.
days = duration // 86_400 % 86_400 % 30
months = duration // 2_592_000 % 2_592_000 % 12
years = duration // 31_104_000 % 31_104_000

msg = ''
if duration >= 31_104_000:
    msg += f'{years} год '
if duration >= 2_592_000:
    msg += f'{months} мес '
if duration >= 86_400:
    msg += f'{days} с '
if duration >= 3_600:
    msg += f'{hours} час '
if duration >= 60:
    msg += f'{minutes} мин '
msg += f'{sec} сек'

print(msg)
