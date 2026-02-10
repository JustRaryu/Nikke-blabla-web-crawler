import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--window-size=1920,1080") # Emulate a full screen
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

#note that you might need to change your openid to yours, check it by opening your blabla profile then click on shiftypad, copy your whole id after the "openid=" part and replace it in the link below
#shouldnt matter if you do or not have all nikkes, it can check anyways
URL_TEMPLATE = "https://www.blablalink.com/shiftyspad/nikke?from=list&nikke={}&openid=MjkwODAtMjgwNTQxODU3OTQ2OTEwMjIxOQ==" 
def scrape_nikkes(start_id, end_id):
    found_characters = []
    
    for nikke_id in range(start_id, end_id + 1):
        target_url = URL_TEMPLATE.format(nikke_id)
        print(f"Checking ID {nikke_id}...", end="\r")
        
        try:
            driver.get(target_url)
            # Give it around a second to fully execute all scripts
            time.sleep(0.8) 
            
            # Get all spans on the page
            spans = driver.find_elements(By.TAG_NAME, "span")
            
            char_name = None
            for s in spans:
                text = s.text.strip()
                # Logic: The name is likely longer than 2 chars, 
                # but not a giant paragraph or the site name.
                if text and text not in ["Blablalink", "Home", "List", "Loading..."] and len(text) < 30:
                    char_name = text
                    break 

            if char_name:
                print(f"✅ ID {nikke_id}: {char_name}")
                found_characters.append([nikke_id, char_name])
            else:
                # If we still fail, let's grab the Page Title as a last resort
                page_title = driver.title
                if "Blablalink" not in page_title:
                    print(f"✅ ID {nikke_id}: {page_title} (from title)")
                    found_characters.append([nikke_id, page_title])
                else:
                    print(f"❌ ID {nikke_id}: Content not loaded.")

        except Exception as e:
            print(f"⚠️ ID {nikke_id}: Error")

    driver.quit()
    save_results(found_characters)

def save_results(data):
    with open('nikke_ids.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Name'])
        writer.writerows(data)
    print(f"\nFinished. Found {len(data)} characters.")

if __name__ == "__main__":
    scrape_nikkes(1, 600) #please note that the real range for is around  600 or something but there are collabs units that ocupy way higher ids, usually in the range of 800s