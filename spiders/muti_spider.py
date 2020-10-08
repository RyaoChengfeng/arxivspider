from multiprocessing import Pool
from spiders import spider


# 多线程爬取论文
def msg():
    r_number_list = spider.get_number()
    for number in r_number_list:
        pool = Pool(processes=12)
        pool.apply_async(spider.get_msg, args=(number,))
        pool.close()
        pool.join()
    print('爬取完成')


# 多线程下载论文
def download():
    r_number_list = spider.get_number()
    for number in r_number_list:
        pool = Pool(processes=12)
        pool.apply_async(spider.get_all_doc, args=(number,))
        pool.close()
        pool.join()
    print('下载完成')


if __name__ == '__main__':
    download()
