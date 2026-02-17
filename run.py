from startups.startups import StartUpsExtractor

with StartUpsExtractor() as bot:
    no_of_pages = int(input("Enter the of pages:"))
    bot.landing_first_page()
    bot.removing_cookie()
    bot.go_to_next_page(no_of_pages)
    bot.csv_to_excel()


