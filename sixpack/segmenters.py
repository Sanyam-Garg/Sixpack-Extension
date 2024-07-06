import random

class SegmenterFactory:

    @staticmethod
    def create_from_rules(segmentation_rules: list):
        segmenter = None
        segmentation_rules = segmentation_rules if segmentation_rules else []
        for rule in reversed(segmentation_rules):
            rule_class, rule_split_A, rule_split_B = rule
            if rule_class == 'random':
                segmenter = RandomSegmenter(rule_split_A, rule_split_B)
            elif rule_class == 'user-agent':
                segmenter = UserAgentSegmenter(rule_split_A, rule_split_B, segmenter)
            elif rule_class == 'location':
                segmenter = LocationSegmenter(rule_split_A, rule_split_B, segmenter)
        
        return segmenter if segmenter else RandomSegmenter()


class RandomSegmenter:

    def __init__(self, split_A=50, split_B=50) -> None:
        self.split_A = split_A
        self.split_B = split_B
        self.fallback = None
    
    def choose(self, request, alternatives: list):
        if random.randint(1, 100) <= self.split_A:
            return alternatives[0]
        return alternatives[1]

class BaseListBasedSegmenter:

    def __init__(self, split_A=None, split_B=None, fallback=None) -> None:
        self.split_A = split_A if split_A else []
        self.split_B = split_B if split_B else []
        self.fallback = fallback if fallback else RandomSegmenter()
    
    def choose(self, request, param, alternatives: list):
        if param in self.split_A:
            return alternatives[0]
        elif param in self.split_B:
            return alternatives[1]
        return self.fallback.choose(request, alternatives)

class UserAgentSegmenter(BaseListBasedSegmenter):

    def __init__(self, split_A=None, split_B=None, fallback=None) -> None:
        super().__init__(split_A, split_B, fallback)
    
    def choose(self, request, alternatives: list):
        user_agent = request.headers.get('User-Agent')
        return super().choose(request, user_agent, alternatives)

class LocationSegmenter(BaseListBasedSegmenter):

    def __init__(self, split_A=None, split_B=None, fallback=None) -> None:
        super().__init__(split_A, split_B, fallback)
    
    def choose(self, request, alternatives: list):
        location = request.headers.get('location') # TODO: check this
        return super().choose(request, location, alternatives)
