from flask import Flask,render_template, request
import pickle
import numpy as np

app=Flask(__name__)

popular_df=pickle.load(open('popular.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
similarity_scores=pickle.load(open('similarity_scores.pkl','rb'))


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_df['Book-Title'].values),
                           book_author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           num_ratings=list(popular_df['num_ratings'].values),
                           avg_rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend_books():
    user_input=request.form.get('user_input')
    data=[]
    try:
        index=np.where(pt.index==user_input)[0][0]    
        similar_items=sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:6]
        for i in similar_items:
            temp=[]
            temp_df=books[books['Book-Title']==pt.index[i[0]]]
            temp.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
            temp.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
            temp.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
            data.append(temp)
    except:
        print("Error")
    
    return render_template('recommend.html',data=data)

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__=='__main__':
    app.run(debug=True)