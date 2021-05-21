# -*- coding: utf-8 -*-
import unittest

from gilded_rose import (Item, GildedRose)


class GildedRoseTest(unittest.TestCase):

    def test_foo(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_goods()
        self.assertEqual("foo", gilded_rose.items[0].name)

    def test_sulfuras_item(self):
        items = [Item(name='Sulfuras, Hand of Ragnaros', sell_in=5, quality=80),
                 Item(name='Sulfuras, Hand of Ragnaros', sell_in=-1, quality=80)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_goods()
        # > 0 days
        self.assertEqual(gilded_rose.items[0].quality, 80)
        self.assertEqual(gilded_rose.items[0].sell_in, 5)
        # < 0 days
        self.assertEqual(gilded_rose.items[1].quality, 80)
        self.assertEqual(gilded_rose.items[1].sell_in, -1)

    def test_quality_decreases_regular_items(self):
        items = [Item(name='Breastplate of the Eagle', sell_in=10, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_goods()
        self.assertEqual(gilded_rose.items[0].quality, 19)
        self.assertEqual(gilded_rose.items[0].sell_in, 9)

    def test_quality_decreases_regular_items_after_expiration(self):
        items = [Item(name='Breastplate of the Eagle', sell_in=0, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_goods()
        self.assertEqual(gilded_rose.items[0].quality, 18)
        self.assertEqual(gilded_rose.items[0].sell_in, -1)

    def test_quality_decreases_regular_items_min_0(self):
        items = [Item(name='Breastplate of the Eagle', sell_in=10, quality=0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_goods()
        self.assertEqual(gilded_rose.items[0].quality, 0)
        self.assertEqual(gilded_rose.items[0].sell_in, 9)

    def test_quality_increases_improving_items(self):
        items = [Item(name='Aged Brie', sell_in=15, quality=0),
                 Item(name='Backstage passes to a TAFKAL80ETC concert', sell_in=15, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_goods()
        # brie
        self.assertEqual(gilded_rose.items[0].quality, 1)
        self.assertEqual(gilded_rose.items[0].sell_in, 14)
        # backstage
        self.assertEqual(gilded_rose.items[1].quality, 21)
        self.assertEqual(gilded_rose.items[1].sell_in, 14)

    def test_quality_increases_improving_items_10_days(self):
        items = [Item(name='Aged Brie', sell_in=10, quality=0),
                 Item(name='Backstage passes to a TAFKAL80ETC concert', sell_in=10, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_goods()
        # brie
        self.assertEqual(gilded_rose.items[0].quality, 1)
        self.assertEqual(gilded_rose.items[0].sell_in, 9)
        # backstage
        self.assertEqual(gilded_rose.items[1].quality, 22)
        self.assertEqual(gilded_rose.items[1].sell_in, 9)

    def test_quality_increases_improving_items_5_days(self):
        items = [Item(name='Aged Brie', sell_in=5, quality=0),
                 Item(name='Backstage passes to a TAFKAL80ETC concert', sell_in=5, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_goods()
        # brie
        self.assertEqual(gilded_rose.items[0].quality, 1)
        self.assertEqual(gilded_rose.items[0].sell_in, 4)
        # backstage
        self.assertEqual(gilded_rose.items[1].quality, 23)
        self.assertEqual(gilded_rose.items[1].sell_in, 4)

    def test_quality_increases_improving_items_0_days(self):
        items = [Item(name='Aged Brie', sell_in=0, quality=0),
                 Item(name='Backstage passes to a TAFKAL80ETC concert', sell_in=0, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_goods()
        # brie
        self.assertEqual(gilded_rose.items[0].quality, 2)
        self.assertEqual(gilded_rose.items[0].sell_in, -1)
        # backstage
        self.assertEqual(gilded_rose.items[1].quality, 0)
        self.assertEqual(gilded_rose.items[1].sell_in, -1)

    def test_quality_not_increases_past_50_improving_items(self):
        items = [Item(name='Aged Brie', sell_in=10, quality=50),
                 Item(name='Backstage passes to a TAFKAL80ETC concert', sell_in=10, quality=50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_goods()
        # brie
        self.assertEqual(gilded_rose.items[0].quality, 50)
        self.assertEqual(gilded_rose.items[0].sell_in, 9)
        # backstage
        self.assertEqual(gilded_rose.items[1].quality, 50)
        self.assertEqual(gilded_rose.items[1].sell_in, 9)

    def test_quality_decreases_conjured_items(self):
        items = [Item(name='Conjured Mana Cake', sell_in=10, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_goods()
        self.assertEqual(gilded_rose.items[0].quality, 18)
        self.assertEqual(gilded_rose.items[0].sell_in, 9)

    def test_quality_decreases_conjured_items_after_expiration(self):
        items = [Item(name='Conjured Mana Cake', sell_in=0, quality=20)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_goods()
        self.assertEqual(gilded_rose.items[0].quality, 16)
        self.assertEqual(gilded_rose.items[0].sell_in, -1)

    def test_quality_decreases_conjured_items_min_0(self):
        items = [Item(name='Conjured Mana Cake', sell_in=10, quality=0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_goods()
        self.assertEqual(gilded_rose.items[0].quality, 0)
        self.assertEqual(gilded_rose.items[0].sell_in, 9)

    def test_quality_decreases_any_conjured_items(self):
        items = [Item(name='Conjured Health Cake', sell_in=10, quality=0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_goods()
        self.assertEqual(gilded_rose.items[0].quality, 0)
        self.assertEqual(gilded_rose.items[0].sell_in, 9)

    def test_quality_decreases_any_backstage_passes(self):
        items = [Item(name='Backstage passes to a SFDK concert', sell_in=10, quality=50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_goods()
        self.assertEqual(gilded_rose.items[0].quality, 50)
        self.assertEqual(gilded_rose.items[0].sell_in, 9)


if __name__ == '__main__':
    unittest.main()
