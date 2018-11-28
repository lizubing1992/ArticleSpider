CREATE TABLE article(
	title VARCHAR(50) NOT NULL COMMENT '标题',
	url VARCHAR(200) NOT NULL COMMENT '文章url路径',
	url_object_id VARCHAR(50) NOT NULL COMMENT '主键id',
	article_type VARCHAR(20) NOT NULL COMMENT '文章类型',
	author_name VARCHAR(20) COMMENT '作者',
	publish_time DATETIME COMMENT '发布时间',
	crawl_time DATETIME COMMENT '爬取时间',
	content LONGTEXT COMMENT '文章内容',
	front_image_url VARCHAR(200) COMMENT '文章封面路径'
)ENGINE=INNODB DEFAULT CHARSET=utf8