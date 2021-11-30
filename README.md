# Shopee_Intern_assessment
flask_assignment_4
承接作業1，我們將利用Flask建立一個查詢文章的API。 這個API的參數有：

q: 可以給定要查詢的字 (可為多個)
n: 回應幾篇文章
w: 每篇文章回應的字數
比如說: https://0.0.0.0:5000/news_api?q=新垣結衣,結婚&n=10&w=50 就會回傳標題或是內文有含"新垣結衣"和"結婚"的文章中，選最多10篇文章，每一篇文章回傳最初的50個字

需求:

api回傳的格式必須要是json格式 （key的名稱自訂)
請上傳原始碼到github，並提供url以供檢查
提供執行之畫面截圖
demo link:
https://flaskass4.herokuapp.com/news_api?q=台灣,疫苗&n=10&w=50
