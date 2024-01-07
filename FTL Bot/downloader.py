import io
import os
import requests
import json
from pytube import YouTube as yt
from name_gen import Random_names
from selenium import webdriver
from errors import VideoTooLongException
from selenium.webdriver.firefox.options import Options as op
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class bot_downloader:
    def __init__(self):
        self.Options = op()
        self.Options.add_argument('--headless')
        self.Options.add_argument('--no-sandbox')

    def __close__(self):
        if self.driver:
            self.driver.quit()

    def Download_video_YT(self,url: str) -> dict[str, str]:
        if url.startswith('https://youtu.be/'):
            id = url.split('https://youtu.be/')[-1].split('?')[0]
            url = f'https://www.youtube.com/watch?v={id}'

        video = yt(url)
        gen_name = Random_names().generate(video.title)

        if video.length > 600:
            raise VideoTooLongException(video.length, 600)

        video.streams.get_by_resolution('720p').download(filename=gen_name+'.mp4')
        path = f'{os.path.abspath(os.curdir)}\\{gen_name}.mp4'
        return path

    def Download_video_Insta(self, url) -> str:
        driver = webdriver.Firefox(options=self.Options)
        driver.get(url)
        css_property_insta = '.x1lliihq.x5yr21d.xh8yej3 video'

        element = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_property_insta )))
        link = element.get_attribute("src")

        return self.write_video(link)

    def Download_Pinterest(self, url):
        driver = webdriver.Firefox(options=self.Options)
        driver.get(url)
        css_property_video = 'script[data-test-id="video-snippet"]'
        css_property_image = 'script[data-test-id="leaf-snippet"]'

        video_flag = None
        try:
            video_flag = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_property_video)))
        except TimeoutException:
            img_flag = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, css_property_image)))

        if video_flag is not None:
            element = driver.execute_script('''function getScriptContent() {
                                                        var scriptElement = document.querySelector('script[data-test-id="video-snippet"]');
                                                        return scriptElement ? scriptElement.textContent : null;}
                                                    return getScriptContent();''')
            link = json.loads(element)['contentUrl']
            driver.quit()
            return self.write_video(link)
        else:
            element = driver.execute_script('''function getScriptContent() {
                                                        var scriptElement = document.querySelector('script[data-test-id="leaf-snippet"]');
                                                        return scriptElement ? scriptElement.textContent : null;}
                                                    return getScriptContent();''')
            link = json.loads(element)['image']
            driver.quit()
            return self.write_photo(link)

    def write_photo(self, link):
            gen_name = Random_names().generate('random')
            with open(f'{gen_name}.png', 'wb') as file:
                with requests.get(link) as res:
                    for chunk in res.iter_content(io.DEFAULT_BUFFER_SIZE):
                        file.write(chunk)
            path = f'{os.path.abspath(os.curdir)}\\{gen_name}.png'
            return path

    def write_video(self, link):
        gen_name = Random_names().generate('random')
        with open(f'{gen_name}.mp4', 'wb') as file:
            with requests.get(link) as res:
                for chunk in res.iter_content(io.DEFAULT_BUFFER_SIZE):
                    file.write(chunk)
        path = f'{os.path.abspath(os.curdir)}\\{gen_name}.mp4'
        return path
