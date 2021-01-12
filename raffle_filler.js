// INIT

const fetch = require('isomorphic-fetch')

// MODIFY

const URL = "https://www.instagram.com/p/CI9RODKnFhU/" // URL of post to scrape
const account_tags_allowed = 2; // number of tags (per account) allowed for scraping

const re_get_username = /(@[^@\s]+)/gm;
const re_get_comments = /({"node":{"id":"(\d+)","text":"(.{0,200})","created_at":\d{8,20},"did_report_as_spam":\w{0,5},"owner":{"id":"(\d{5,20})","is_verified":(\w{0,5}),"profile_pic_url":"[^,]{0,260}","username":"(.{0,25})"},"viewer_has_liked":(\w{0,5}),"edge_liked_by":{"count":(\d{1,9})},"is_restricted_pending":\w{0,5},"edge_threaded_comments":{"count":(\d{1,9}),"page_info":{"has_next_page":\w{0,5},"end_cursor":\w{0,5}},"edges":\[.{0,1000}\]}}}(,?))/gm;


(async () => {
  try {
    const response = await fetch(URL);
  	const HTML = await response.text();
  	// console.log(HTML); 
  	// const re_get_num_comments = new RegExp('\\"edge_media_to_parent_comment\\"\\:\\{\\"count\\"\\:(\\d+)\\,');
  	// const count_match = await HTML.match(re_get_num_comments);
  	// console.log("Comment count:", count_match[1]);
  	// const re_get_comments = new RegExp('({"node":{"id":"(\\d+)","text":"(.{0,200})","created_at":\\d{8,20},"did_report_as_spam":\\w{0,5},"owner":{"id":"(\\d{5,20})","is_verified":(\\w{0,5}),"profile_pic_url":"[^,]{0,260}","username":"(.{0,25})"},"viewer_has_liked":(\\w{0,5}),"edge_liked_by":{"count":(\d{1,9})},"is_restricted_pending":\\w{0,5},"edge_threaded_comments":{"count":(\\d{1,9}),"page_info":{"has_next_page":\\w{0,5},"end_cursor":\\w{0,5}},"edges":\\[.{0,1000}\\]}}}(,?))', 'gm')
  	const match_iter = await HTML.matchAll(re_get_comments);
  	// console.log(HTML);
  	// INIT 2
  	let m; // temp var

  	let user_id;
  	let text;
  	let two_tags;
  	let time;
  	let username;


  	var dict = {} // init output dictionary
  	// text processing init vars 
  	var count_matches = 0;
  	var count_account_tags = 0;

  	for (const match of match_iter) {
  		// get user id
  		user_id = match[2];
  		
  		// get text of comment 
  		text = match[3];
  		// text processing
  		var tagged_accounts_array = new Array();
  		const match_text_iter = text.matchAll(re_get_username);
  		count_account_tags = 0;
  		for (const match_arr of match_text_iter) {
  			if (count_account_tags == account_tags_allowed) {
  				break;
  			} else {
  				// console.log(tagged_accounts_array);
  				tagged_accounts_array.push(match_arr[0]);
  			}
  		} 

  		// get UTC time of comment 
  		time = match[4];

  		// get username 
  		username = match[6];

  		// STORE in JS object (output JSON) 
  		// (in order of appearance in actual HTML)
  		dict[user_id] = {}   // init inner dict (dict for each user)
  		dict[user_id]["text"] = tagged_accounts_array;
  		dict[user_id]["time"] = time;
  		dict[user_id]["username"] = username;
  		count_matches++; // counting matches
  	}
  	console.log("Total Comments Scraped:", count_matches); // print total comments scraped 
  	console.log(dict); 

  } catch(err) {
    console.log(err); // error catching
  }
})();
