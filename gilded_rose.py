# -*- coding: utf-8 -*-
class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)


class RegularItem(Item):
    quality_change = -1
    max_quality = 50

    def update_sell_in(self):
        self.sell_in -= 1

    def update_quality(self):
        self.quality += self.quality_change

    def check_boundary_conditions(self):
        if self.quality > self.max_quality:
            self.quality = self.max_quality
        elif self.quality < 0:
            self.quality = 0

    def next_day(self):
        # simulate day passing
        self.update_sell_in()
        self.update_quality()
        # goods decrease twice as fast when expired
        if self.sell_in < 0:
            self.update_quality()
        self.check_boundary_conditions()


class AgedBrie(RegularItem):
    # quality increases over time
    quality_change = 1


class BackstagePasses(RegularItem):
    # quality increases over time
    quality_change = 1

    def update_quality(self):
        # quality based on time until sell_in
        # TODO might be done better with dictionary of ranges, but how to get <0 lower bound, >10 upper bound
        self.quality += self.quality_change
        if self.sell_in < 10:
            self.quality += self.quality_change
        if self.sell_in < 5:
            self.quality += self.quality_change
        if self.sell_in < 0:
            self.quality = 0


class Sulfuras(RegularItem):
    max_quality = 80

    # do not change quality
    def update_quality(self):
        pass

    # no need to sell
    def update_sell_in(self):
        pass


class ConjuredItem(RegularItem):
    quality_change = -2


def categorise_item(item):
    if 'Sulfuras' in item.name:
        return Sulfuras(item.name, item.sell_in, item.quality)
    elif 'Backstage passes' in item.name:
        return BackstagePasses(item.name, item.sell_in, item.quality)
    elif 'Aged Brie' in item.name:
        return AgedBrie(item.name, item.sell_in, item.quality)
    elif 'Conjured' in item.name:
        return ConjuredItem(item.name, item.sell_in, item.quality)
    else:
        return RegularItem(item.name, item.sell_in, item.quality)


class GildedRose(object):

    def __init__(self, items):
        self.items = []
        # populate stock with categorised items
        for item in items:
            self.items.append(categorise_item(item))

    def update_goods(self):
        for item in self.items:
            item.next_day()
