from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from datetime import datetime, date,timedelta
import time
import json 
from conectionES import ConectionES

driver = webdriver.Chrome('./chromedriver')
#Noticia1
#url='https://www.facebook.com/elcomercio.pe/posts/10158625323708836'
#Noticia2
url = 'https://www.facebook.com/peru21/posts/10157038052210868'
#Notica3
#url = 'https://www.facebook.com/peru21/posts/10157038583560868'
#url="https://www.facebook.com/elcomercio.pe/videos/vb.71263708835/424766364830484/"
#url='https://www.facebook.com/independenciaprestamos/photos/a.1490503960986926/2309279159109398/'
driver.get(url)
driver.execute_script('var XHR=XMLHttpRequest.prototype,open=XHR.open,send=XHR.send,NumberElementArray=1;XHR.open=function(e,t){return this._method=e,this._url=t,open.apply(this,arguments)},XHR.send=function(e){return this.addEventListener("load",function(){if(this._method,this._url,this.response,this._url.search("api/graphql")>=0&&(console.log(this._url),console.log(e),e.search("displayCommentsFeedbackContext")>=0)){var t=document.createElement("input");t.setAttribute("name","json_facebook_post_comment"),t.setAttribute("value",this.response),t.setAttribute("id","json_facebook_post_comment"+NumberElementArray.toString()),t.setAttribute("type","hidden");var n=document.getElementById("div1");document.body.insertBefore(t,n),NumberElementArray+=1,console.log("NumberElementArray",NumberElementArray)}}),send.apply(this,arguments)};')
try:
	element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,'u_0_c'))
    )
	driver.execute_script('document.getElementById("u_0_c").remove();')

except Exception as e:
	print('no existe el elemento')

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,'headerArea'))
    )
    driver.execute_script('document.getElementById("headerArea").remove();')

except Exception as e:
    print('no existe el elemento')

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,'//form[@class="commentable_item collapsed_comments"]//a[@data-testid="UFI2CommentsCount/root"]'))
    )
element.click()

element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,'//form[@class="commentable_item collapsed_comments"]//a[@data-testid="UFI2ViewOptionsSelector/link"]'))
    )
element.click()

element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,'//li[3]/a/span/span/div[@data-testid="UFI2ViewOptionsSelector/menuOption"]'))
    )
element.click()

time.sleep(10)

while True:
    error = False
    try:
        element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH,'//a[@data-testid="UFI2CommentsPagerRenderer/pager_depth_0"]'))

        ) 
        element.click()
        
        #encontrar el elemento por el XPATH
        rpta = driver.find_elements_by_xpath('//a[@data-testid="UFI2CommentsPagerRenderer/pager_depth_1"]')
        #por cada elemento encontrado hacer click
        for links in rpta:
            links.click()

    except Exception as e:
        print(e)
        print('error de elemento')
        error = True
    if(error):
        break
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # error = False
    # try:
        
    #     element.click()
    # except Exception as e:
    #     print(e)
    #     print('no se encontro elemento')
    #     error = True
    # if(error):
    #     break
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # time.sleep(1)

try:
    listElementComment = driver.find_elements_by_name("json_facebook_post_comment")
except Exception as e:
    print(e)

db = ConectionES()
for elementComment in listElementComment:
    jsonElementComment = json.loads(elementComment.get_attribute("value"))
    listComment = []
    try:
        listComment = jsonElementComment.get('data').get('feedback').get('display_comments').get('edges')
    except Exception as e:
        print(e)
    for comment in listComment:
        id = comment.get('node').get('id')
        data = comment.get('node')
        print(json.dumps(data))
        db.es.index(index='facebook_post_comment',doc_type='employee',id=id,body=data)
        pass
    pass

'''
a = json.loads(element.text)
print(a)
driver.execute_script('document.getElementById("json_facebook_post_comment").remove();')
'''
driver.close()