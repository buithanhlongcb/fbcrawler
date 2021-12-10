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

Make sure that all the requirements are satisfied. You may clone this repository and then navigate to the top folder: the first fbcrawler and then run the launch the application with:


```shell
scrapy crawl fb -a page_id="us.vunhcm" -o hcmus1.csv
```


```shell
scrapy crawl post -a post_url="https://www.facebook.com/SMTOWNVietnamFC/photos/a.233526290182736/1830558797146136" -o hcmus.csv
```

