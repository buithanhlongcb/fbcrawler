# Crawl Facebook Comment With Scrapy

## Disclaimer

This project is not authorized by Facebook and does not follow the Facebook's [robots.txt](https://www.facebook.com/robots.txt). Scraping without Facebook's permission is a violation of the [terms and conditions of scraping](https://www.facebook.com/apps/site_scraping_tos_terms.php). However, this project is only for educational purposes to illustrate the use of Scrapy.

## Collaborators

| Student's ID | Name                     | Github                                               |
| ------------ | ------------------------ | ---------------------------------------------------- |
| 18127132     | Bùi Thành Long           | [@buithanhlongcb](https://github.com/buithanhlongcb) |
| 18127187     | Dương Ngọc Nguyên Phương | [@dnnphuong](https://github.com/dnnphuong)           |
| 18127196     | Cao Nguyễn An Sơn        | [@ansoncaonguyen](https://github.com/ansoncaonguyen) |
| 18127197     | Đặng Khánh Sơn           |                                                      |

## Installation

Requirements: You need to have **Python 3** and the **Scrapy** framework that can install by using

`pip install scrapy`

## How to run

Make sure that all the requirements are satisfied. You may clone this repository and then navigate to the top folder: the first fbcrawler and then launch the application with:

### Crawl comments from a page

This `spider` will crawl comments from 5 most related posts from a Facebook page.

You need to login to Facebook and also provide the Page's ID.


```shell
scrapy crawl fb -a email="your_email@gmail.com" -a password="your_password" -a page_id="us.vnuhcm" -o hcmus1.csv
```

### Crawl comments from a post

This spider will crawl comments from a post and will not need to login.


```shell
scrapy crawl post -a post_url="your_post_link" -o sm.csv
```

However, you have to make sure that your post link will have some structure below:

- https://www.facebook.com/SMTOWNVietnamFC/photos/a.233526290182736/1830558797146136

- https://www.facebook.com/569114550176938/posts/1402548096833575/

