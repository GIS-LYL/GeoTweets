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

// ���ӵ�mongodb
$m = new MongoClient();

// ѡ��һ�����ݿ�
$db = $m->test;

// ѡ��һ������
$collection = $db->Domain;

// ��ѯ�ĵ���ȷ����̨�Ѽ�����ؼ���
$amount = $collection->count(array('domain' => 'Culture'));

if($amount == 0)//����δ�����������ýű�
{
    $status = exec('python E:\PythonProject\Twitter\Test\GetKeywords.py');
    if($status == 'finished')
    {
        exec('python E:\PythonProject\Twitter\Test\AcquireTwitters.py');
    }
}
else//��̨�Ѿ�������ؼ���
{

}

$domain = "";

if($_SERVER['REQUEST_METHOD'] == 'POST')//���ύ������
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

    $jsonData = json_encode($arr);//ת����json����
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
        $jsonData = json_encode($arr);//ת����json����
        echo $jsonData;
        if($cursor->hasNext())
            echo ',';
    }
    echo ']}';*/

    //�����ݿ⣬���twitter��importance���Ƿ����domain�����У�������ڷ��������У�������������ʾ
    //��û�У�����python�ű�����ȡtwitter���������ݿ⡣�����ݿ��л�ȡ����twitter�������domain��keywords��importance����ɺ󷵻ظ�php
    //ok��Ȼ��php�ٴ����ݿ��в顣
    exec('python E:\PythonProject\Twitter\Test\TextMining.py Culture');//ִ�У����������ֵ���������
    //system('python E:\PythonProject\Twitter\Test\TextMining.py Culture');//ִ�У��������ֵ���������

}

?>

</body>
</html>