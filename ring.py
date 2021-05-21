from __future__ import annotations

import typing as t

from collections import OrderedDict


T = t.TypeVar('T')


class RingLink(object):

    def __init__(self, content: object):
        self.content = content
        self.next: t.Optional[RingLink] = None
        self.previous: t.Optional[RingLink] = None


class Ring(t.Generic[T]):

    def __init__(self, content: t.Iterable[T], link_type: t.Type[RingLink] = RingLink):
        self._content: OrderedDict[T, RingLink] = OrderedDict(
            {content: link_type(content) for content in content}
        )

        _content = tuple(self._content.values())

        for i in range(len(_content)):
            _content[i].next = _content[(i + 1) % len(_content)]
            _content[i].previous = _content[i - 1]

        try:
            self._current = _content[-1]
        except IndexError:
            raise ValueError('Ring must contain at least one object')

    @property
    def all(self) -> t.Collection[T]:
        return self._content.keys()

    def current(self) -> T:
        return self._current.content

    def next(self) -> T:
        self._current = self._current.next
        return self._current.content

    def previous(self) -> T:
        self._current = self._current.previous
        return self._current.content

    def peek_next(self) -> T:
        return self._current.next.content

    def peek_previous(self) -> T:
        return self._current.previous.content

    def loop_from(self, start: T) -> t.Iterator[T]:
        link = self._content[start]
        while True:
            yield link.content
            link = link.next
            if link.content == start:
                break

    def after(self, item: T) -> T:
        return self._content[item].next.content

    def before(self, item: T) -> T:
        return self._content[item].previous.content

    def __iter__(self) -> t.Iterable[T]:
        while True:
            yield self.next()

    def __len__(self):
        return self._content.__len__()

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, self.__class__)
            and self.all == other.all
        )
