from ._abstract import AbstractScraper

from .consts import TIME_REGEX, HTML_SYMBOLS


class ThePioneerWoman(AbstractScraper):

    @classmethod
    def host(self):
        return 'thepioneerwoman.com'

    def publisher_site(self):
        return 'http://thepioneerwoman.com/'

    def title(self):
        return self.soup.find('h3', {'class': 'recipe-title'}).get_text()

    def total_time(self):
        dds = [
            dd.get_text(strip=True) for dd in
            self.soup.find('div', {'class': 'recipe-summary-time'}).findAll('dd')
        ]

        total_minutes = 0

        for dd in dds:
            try:
                matched = TIME_REGEX.search(dd)
                if matched is None:
                    raise AttributeError

                total_minutes += int(matched.groupdict().get('minutes') or 0)
                total_minutes += 60 * int(matched.groupdict().get('hours') or 0)

            except AttributeError:  # when there is no span or no time regex match
                pass

        return total_minutes

    def ingredients(self):
        ingredients_html = self.soup.find('ul', {'class': "list-ingredients"}).findAll('li')

        return [
            ingredient.get_text(strip=True)
            for ingredient in ingredients_html
        ]

    def instructions(self):
        instructions_html = self.soup.findAll('div', {'class': 'panel-body'})[-1]
        return instructions_html.get_text(strip=True)