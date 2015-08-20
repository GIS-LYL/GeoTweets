<!DOCTYPE html>
<html>
<head>
    <title>GeoTweets 1234567890</title>
    <meta charset="utf-8">
</head>
<body>

<h1>GeoTweets</h1>
<form method = "post" action = "<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>">
    Domain:<select name= "domains">
        <option value = "History">History</option>
        <option value = "Culture">Culture</option>
        <option value = "Sport">Sport</option>
    </select>

    <input type="submit" name="submit" value="Submit">
</form>

<?php

// 连接到mongodb
$m = new MongoClient();

// 选择一个数据库
$db = $m->test;

// 选择一个集合
$collection = $db->Domain;

// 查询文档，确定后台已计算出关键词
$amount = $collection->count(array('domain' => 'Culture'));

if($amount == 0)//若还未计算出，则调用脚本
{
    $status = exec('python E:\PythonProject\Twitter\Test\GetKeywords.py');
    if($status == 'finished')
    {
        exec('python E:\PythonProject\Twitter\Test\AcquireTwitters.py');
    }
}
else//后台已经计算出关键词
{

}

$domain = "";

if($_SERVER['REQUEST_METHOD'] == 'POST')//若提交了请求
{
    $domain = $_POST['domains'];

    $arr = array('type' => 'FeatureCollection', 'id' => 'tweetsyoulike.c22ab257',
        'features' => array());

    $collection = $db->Twitter;

    $cursor = $collection->find();
    $i = 1;
    while($cursor->hasNext())
    {
        $document = $cursor->getNext();

        $arr['features'][] = array('type' => 'Feature', 'id' => $document['_id'],
            'geometry' => array('coordinates' => $document['coordinates'], 'type' => 'Point'),
            'properties' => array('id' => $document['_id'], 'time' => $document['created_at'],
                'name' => $document['name'], 'text' => $document['text'], 'location' => $document['location'],
                'media' => $document['media_url'], 'marker-size' => 'medium',
                'marker-color' => '#7ec9b1', 'marker-symbol' => '3',
                'importance' => $document['importance']));
    }

    $jsonData = json_encode($arr);//转换成json数据
    echo $jsonData;

    /*echo '{"type":"FeatureCollection","id":"tweetsyoulike.c22ab257","features":[';

    $collection = $db->Twitter;
    $cursor = $collection->find();
    $i = 1;
    while($cursor->hasNext())
    {
        $document = $cursor->getNext();
        $arr = array('type' => 'Feature', 'id' => $document['_id'],
            'geometry' => array('coordinates' => $document['coordinates'], 'type' => 'Point'),
            'properties' => array('id' => $document['_id'], 'time' => $document['created_at'],
                'name' => $document['name'], 'text' => $document['text'], 'location' => $document['location'],
                'media' => $document['media_url'], 'marker-size' => 'medium',
                'marker-color' => '#7ec9b1', 'marker-symbol' => '3',
                'importance' => $document['importance']));
        $jsonData = json_encode($arr);//转换成json数据
        echo $jsonData;
        if($cursor->hasNext())
            echo ',';
    }
    echo ']}';*/

    //查数据库，检查twitter的importance中是否包含domain，若有，结果存在返回数组中，排序后可用来显示
    //若没有，调用python脚本来获取twitter，插入数据库。从数据库中获取所有twitter，计算对domain的keywords的importance，完成后返回给php
    //ok，然后php再从数据库中查。
    exec('python E:\PythonProject\Twitter\Test\TextMining.py Culture');//执行，不输出返回值，保留结果
    //system('python E:\PythonProject\Twitter\Test\TextMining.py Culture');//执行，输出返回值，保留结果

}

?>

</body>
</html>