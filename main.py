import datetime
import time
import requests
import json
from tqdm import tqdm
from bs4 import BeautifulSoup
from sys import path
from os import getcwd, chdir
print(" Old cwd = " + getcwd())#取得當前系統環境位置
chdir('D:/data/Desktop/')#path[0])#將當前環境位置設為當前"檔案位置"
print(" New cwd = " + getcwd())
print("========================")

def Download_media(media_URL,ext):
	#顯示圖片訊息 show image information
	r = get(media_URL)
	total = int(r.headers.get("content-length"))
	print("  影像網址(media URL):\n  ",media_URL)
	print("  檔案容量(file Size): ", round(total /(1024),2), "kB")
	#下載影像 Download media
	fileName = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S%f")+ ext
	file=open(fileName,'wb')
    for data in tqdm(iterable=r.iter_content(chunk_size=1024), total=total / 1024, unit="kB"):
        file.write(data)
    file.close()
	print("  下載完成(Download completed)")
	
def Download_Instagram_Image_1(URL):
	print("Downloading image...")
	#取得圖片網址 get image url
	f = requests.get(URL)
	soup = BeautifulSoup(f.text,'html.parser')
	metaTag = soup.find_all('meta', {'property':'og:image'})
	imgURL = metaTag[0]['content']
	# DownloadImage
	Download_media(imgURL,'.jpg')
	
def Download_Instagram_Image_2(URL):
	print('Downloading image...')
	#get image url
	imgURL=(fileURL.split('?')[0])+'media/?size=l'
	#DownloadImage
	Download_media(imgURL,'.jpg')

def Download_Instagram_media(URL):
	print('Downloading media...')
	try :
		f = requests.get(URL)
		soup = BeautifulSoup(f.text,'html.parser')
		metaTag = soup.find_all('meta',{'property':'al:ios:url'})
		media_id = (metaTag[0]['content']).split('?id=')[1]
	except:
		print('網址錯誤(url error)')
		input('按enter結束')
		exit(0)
	##=====set ds_user_id==========
	# 從瀏覽器的開發者選項中找 "info/"的標頭找User settings1和User settings2對應的資料
	ds_user_id = User settings1
	## 設定標頭 set headers:
	headers={
	'cookie': f'ds_user_id={ds_user_id}; sessionid={ds_user_id}:RRVTsrk8MzDDoj:17;',
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35',
	'x-ig-app-id': User settings2
	}
	media_URL = []
	media_type = ''
	try :
		# 取得頁面訊息 get page information
		media_dataURL = f'https://www.instagram.com/api/v1/media/{media_id}/info/'
		media_data = requests.get(media_dataURL,headers=headers)
		data = json.loads(media_data.text)
		# print(json.dumps(data,indent=2,ensure_ascii=False))
		# input()
		try :
			try : #有影片時
				media_URL = [data['items'][0]['video_versions'][0]['url']]
				media_type = 'video'
			except : 
				media_URL = [data['items'][0]['image_versions2']["candidates"][0]['url']]
				media_type = 'image'
		except :
			media_num=data['items'][0]['carousel_media_count']
			print("  圖片數(number of images):",media_num)
			media_i=data['items'][0]['carousel_media']
			for i in range(media_num):
				media_URL.append(media_i[i]['image_versions2']["candidates"][0]['url'])
				media_type = 'image'
	except:
		print('標頭異常(headers error)')
		input('按enter結束')
		exit(0)
	# 顯示影像訊息並下載 show media information and Download Image
	for i in range(len(media_URL)):
		print(f'{i}.')
		EXT = '.mp4' if (media_type=='video') else '.jpg'
		Download_media(media_URL[i],EXT)

if __name__ == '__main__':
	url = input('輸入網址(Enter URL):')
	while url != '':
		# Download_Instagram_Image_1(url)
		# Download_Instagram_Image_2(url)
		Download_Instagram_media(url)
		
		print("========================")
		url = input('輸入網址(Enter URL):')
