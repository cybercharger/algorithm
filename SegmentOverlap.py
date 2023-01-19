from typing import List, Tuple


class SegmentInfo:
    def __init__(self, start: int, end: int, sid: int, gid: int):
        self.start = start if start <= end else end
        self.end = end if start <= end else start
        self.sid = sid
        self.gid = gid

    def __repr__(self) -> str:
        return f'(s:{self.start}, e:{self.end}, i:{self.sid}, g:{self.gid})'


class SegmentOverlap:
    @staticmethod
    def calc_overlap(s1: int, e1: int, s2: int, e2: int) -> int:
        if s1 > e1:
            s1, e1 = e1, s1
        if s2 > e2:
            s2, e2 = e2, s2
        return max(0, min(e1, e2) - max(s1, s2))

    @staticmethod
    def calc_max_overlap_bruteforce(group1: List[Tuple[int, int]], group2: List[Tuple[int, int]]) -> int:
        if group1 is None or group2 is None:
            return 0

        max_overlap = 0
        for seg_a in group1:
            for seg_b in group2:
                max_overlap = max(max_overlap, SegmentOverlap.calc_overlap(seg_a[0], seg_a[1], seg_b[0], seg_b[1]))

        return max_overlap

    @staticmethod
    def cal_max_overlap(group1: List[Tuple[int, int]], group2: List[Tuple[int, int]]) -> int:
        if group1 is None or group2 is None or len(group1) == 0 or len(group2) == 0:
            return 0

        starts1 = sorted([SegmentInfo(start=p[0], end=p[1], sid=i, gid=0) for i, p in enumerate(group1)], key=lambda x: x.start)
        starts2 = sorted([SegmentInfo(start=p[0], end=p[1], sid=i, gid=1) for i, p in enumerate(group2)], key=lambda x: x.start)
        starts = [starts1, starts2]

        ends1 = [SegmentInfo(start=p[0], end=p[1], sid=i, gid=0) for i, p in enumerate(group1)]
        ends2 = [SegmentInfo(start=p[0], end=p[1], sid=i, gid=1) for i, p in enumerate(group2)]
        ends = sorted(ends1 + ends2, key=lambda x: x.end)

        # cur[0] is the pointer for top of sorted start points of group1
        # cur[1] is the pointer for top of sorted start points of group2
        cur = [0, 0]
        max_overlap = 0
        for segment in ends:
            target_group = starts[segment.gid]
            if segment.sid != target_group[cur[segment.gid]].sid:
                continue
            max_overlap = max(max_overlap, segment.end - max(starts[0][cur[0]].start, starts[1][cur[1]].start))

            # find the next segment not covered by current segment
            while target_group[cur[segment.gid]].end <= segment.end:
                cur[segment.gid] += 1
                if cur[segment.gid] >= len(starts[segment.gid]):
                    return max_overlap

        return max_overlap

    @staticmethod
    def cal_max_overlap_of_groups(groups: List[List[Tuple]]) -> int:
        if groups is None:
            return 0

        for g in groups:
            if g is None or len(g) == 0:
                return 0

        starts = []
        ends = []
        for gid, group in enumerate(groups):
            starts.append(sorted([SegmentInfo(start=p[0], end=p[1], sid=i, gid=gid) for i, p in enumerate(group)], key=lambda x: x.start))
            ends += [SegmentInfo(start=p[0], end=p[1], sid=i, gid=gid) for i, p in enumerate(group)]
        ends = sorted(ends, key=lambda x: x.end)

        # cur[n] is the pointer for top of sorted start points of group_n
        cur = [0] * len(groups)
        max_overlap = 0
        max_start = max([s[0].start for s in starts])
        for segment in ends:
            target_group = starts[segment.gid]
            if segment.sid != target_group[cur[segment.gid]].sid:
                continue

            max_overlap = max(max_overlap, segment.end - max_start)

            # find the next segment not covered by current segment
            while target_group[cur[segment.gid]].end <= segment.end:
                cur[segment.gid] += 1
                if cur[segment.gid] >= len(starts[segment.gid]):
                    return max_overlap
            max_start = max(max_start, starts[segment.gid][cur[segment.gid]].start)

        return max_overlap
