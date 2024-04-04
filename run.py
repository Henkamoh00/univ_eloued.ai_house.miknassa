from miknassa import createApp
app = createApp()

if __name__ == '__main__':
    app.run(debug=False)


# الاوامر المستخدمة في حال العمل بالميقرايشن
# flask db init
# flask db migrate -m "Initial migration"
# flask db upgrade
