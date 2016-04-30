#!/usr/bin/env python
import urllib2
import json
import datetime



def create_post_url(graph_url, APP_ID, APP_SECRET): 
	#create authenticated post URL
	post_args = "/posts?fields=full_picture%2Ccreated_time%2Cname%2Clink%2Cmessage%2Cobject_id%2Cshares%2Cstatus_type&access_token=" + APP_ID + "|" + APP_SECRET
	post_url = graph_url + post_args
    
	return post_url
	
def render_to_json(graph_url):
	#render graph url call to JSON
	web_response = urllib2.urlopen(graph_url)
	readable_page = web_response.read()
	json_data = json.loads(readable_page)
	
	return json_data

def scrape_posts_by_date(graph_url, date, post_data, APP_ID, APP_SECRET):
	#render URL to JSON
	page_posts = render_to_json(graph_url)
	
	#extract next page
	next_page = page_posts["paging"]["next"]
	
	#grab all posts
	page_posts = page_posts["data"]
	
	#boolean to tell us when to stop collecting
	collecting = True
	
	#for each post capture data
	for post in page_posts:
		try:
			likes_count = get_likes_count(post["id"], APP_ID, APP_SECRET)
			current_post = [[post["id"], post["message"], likes_count, post["shares"]["count"], post["created_time"], post["object_id"], post["status_type"], post["full_picture"]]			

		except Exception:
			current_post = [ "error", "error", "error", "error","error", "error", "error", "error"]
		

		if current_post[4] != "error":
			print date
			print current_post[4]
			if date <= current_post[4]:
				post_data.append(current_post)
				
			elif date > current_post[4]:
				print "Done collecting"
				collecting = False
				break
	
	
	#If we still don't meet date requirements, run on next page			
	if collecting == True:
		scrape_posts_by_date(next_page, date, post_data, APP_ID, APP_SECRET)
	
	return post_data
		
def write_post_data_to_file(post_data, filename):
	
	with open(filename, 'w+') as csvfile:
    		csvwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    	for post in post_data:
    		csvwriter.writerow([post[0], post[1], post[2],post[3],post[4],post[5],post[6],post[7] ])

def get_likes_count(post_id, APP_ID, APP_SECRET):
	#create Graph API Call
	count_likes = 0
#	graph_url = "https://graph.facebook.com/" 
#	likes_args = post_id + "/likes?summary=true&key=value&access_token" + APP_ID + "|" + APP_SECRET
#	likes_url = graph_url + likes_args
#	likes_json = render_to_json(likes_url)

	#pick out the likes count
#	count_likes = likes_json["summary"]["total_count"]

	return count_likes
	
def main():
	#simple data pull App Secret and App ID
	APP_SECRET = "68a6cf69543461c285c641f25213c048"
	APP_ID = "1126789970707224"
	

	graph_url = "https://graph.facebook.com/v2.6/610780312323804"
	
	#the time of last weeks crawl
	last_crawl = datetime.datetime.now() - datetime.timedelta(weeks=5)
	last_crawl = last_crawl.isoformat()
					
		
	#extract post data
	post_url = create_post_url(graph_url, APP_ID, APP_SECRET)
		
	post_data = []
	post_data = scrape_posts_by_date(post_url, last_crawl, post_data, APP_ID, APP_SECRET)
	write_post_data_to_file("facebook-posts.csv",post_data)
		
		
	print post_data
			
	

if __name__ == "__main__":
	main()    