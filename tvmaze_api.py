import urllib.request
import urllib.parse
import json

class Show():
	 def __init__(self, show_id=None, full_info=None):
	 	self.full_info = full_info
	 	if show_id:
	 		self.get_full_info(show_id)
	 	if not (show_id or quick_info or full_info or search_info):
	 		raise ValueError('Atleast one arg needs a value')

	 def get_full_info(self, show_id):
	 	try:
	 		next_episode= urllib.request.urlopen('http://api.tvmaze.com/shows/{}?embed=nextepisode'.format(show_id)).read().decode("utf-8")
	 		next_ep_data= json.loads(next_episode)
	 		self.full_info = next_ep_data
	 	except:
	 		return "Show Not Found"

	 @property
	 def name(self):
	 	try:
	 		if self.full_info:
	 			return self.full_info['name']
	 	except:
	 		return "Show Not Found"
	 @property
	 def status(self):
	 	try:
	 		if self.full_info:
	 			return self.full_info['status']
	 	except:
	 		return None

	 def image(self):
	 	try:
	 		if self.full_info:
	 			return self.full_info['image']['medium']
	 	except:
	 		return None
	 @property
	 def tv_show_id(self):
	 	try:
	 		if self.full_info:
	 			return self.full_info['id']
	 	except:
	 		return "Show Not Found"

	 @property
	 def network(self):
	 	try:
	 		if self.full_info:
	 			return self.full_info['network']['name']
	 		elif self.search_info:
	 			return self.search_info['network']['name']
	 	except:
	 		return None

	 @property
	 def air_date(self):
	 	if self.full_info['status'] == 'Ended':
	 		return "Show has ended"
	 	try:
	 		if self.full_info:
	 			return self.full_info['_embedded']['nextepisode']['airstamp']
	 	except:
	 		return None

	 @property
	 def next_ep_summary(self):
	 	try:
	 		if self.full_info:
	 			ep_sum = self.full_info['_embedded']['nextepisode']['summary']
	 			if "<p>" in ep_sum:
	 				ep_sum = ep_sum.replace("<p>", "")
	 				ep_sum = ep_sum.replace("</p>", "")
	 			elif ep_sum == "":
	 				ep_sum = "No Summary"
	 		return ep_sum
	 	except:
	 		return "No Summary Found"
	 @property
	 def curr_season(self):
	 	try:
	 		if self.full_info:
	 			return self.full_info['_embedded']['nextepisode']['season']
	 	except:
	 		return None
	 @property
	 def curr_episode(self):
	 	try:
	 		if self.full_info:
	 			return self.full_info['_embedded']['nextepisode']['number']
	 	except:
	 		return None


def get_show_details(input):
	try:
		response = urllib.request.urlopen('http://api.tvmaze.com/singlesearch/shows?q={}'.format(input)).read().decode("utf-8")
	except:
		return None
	data = json.loads(response)
	tv_id = data['id']
	tv = Show(show_id=tv_id)
	return tv