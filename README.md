# 颱風放假通知 API

目前颱風假的發佈，主要是各地方政府自行發佈，然後會統整到人事總處的[專屬網頁]((https://www.dgpa.gov.tw/typh/daily/nds.html))上。發佈時間上會延遲至少 30 分鐘（根據 2016 的問答回覆），然後網站上刊登出公布訊息，又會比他們收到訊息再延遲五分鐘。也就是這網頁每五分鐘會自動更新一次，但上面刊登的訊息是五分鐘前的結果。所以比起實際訊息發佈會大約慢個至少 30 分鐘以上）

另外人事總處也有發佈一個 [CAP 格式開放資料的颱風停班停課的 RSS 和 KMZ](https://data.gov.tw/dataset/20457)。但這些東西不知道是否太少人用？裡面的資訊公布比起網站上發佈更是延遲到不可思議的地步。

所以目前可以說沒有一個「可靠可用」的颱風假發佈通知 API。對很多人來說，可能有沒有 API 也不是很重要的事，畢竟要不要放假，大家都是守在電視或網路前，第一時間媒體報導就會得知結果。

但有 API 的好處是，可以自動介接停班停課後該處理的「程序」。例如自動發佈訊息等。

這邊我試著從[人事行政總處通知網頁](https://www.dgpa.gov.tw/typh/daily/nds.html)來建立最新停班停課通知的 API，同時針對發佈的訊息，做一個資料標準化的作業。



# 資訊網頁

https://www.dgpa.gov.tw/typh/daily/nds.html

停班停課資訊

```html
<div class="Header_YMD">113年 10月 3日 天然災害停止上班及上課情形</div>
```

資訊更新時間

```html
<div class="f_right Content_Updata">
  <h4 style="font-weight:normal">
    更新時間：2024/10/03 19:31:12
    <br />
    <a href="https://www.dgpa.gov.tw/informationlist?uid=374" class="f_right color_blue">
      歷次天然災害停止上班上課訊息
    </a>
  </h4>
</div>
```

各地方政府停班停課資訊

```html
<tbody class="Table_Body">
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>基隆市</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>臺北市</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>新北市</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>桃園市</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>新竹市</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>新竹縣</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>苗栗縣</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>臺中市</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>彰化縣</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>雲林縣</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>南投縣</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>嘉義市</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>嘉義縣</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>臺南市</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>高雄市</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>屏東縣</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>宜蘭縣</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>花蓮縣</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>臺東縣</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>澎湖縣</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>連江縣</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font>
    </td>
  </tr>
  <tr>
    <td headers="city_Name" valign="center" align="middle" width="13%"><font>金門縣</font></td>
    <td headers="StopWorkSchool_Info" valign="center" align="left" width="70%">
      <font color="#FF0000">今天停止上班、停止上課。 </font><br /><font color="#000080">明天照常上班、照常上課。 </font>
    </td>
  </tr>
  <!-- 備註 #a5a1c2-->
  <tr style="background:rgba(204, 124, 236, 0.39);">
    <td colspan="3">
      <p>1.若欲進入本總處網站首頁版面，請按<a href="https://www.dgpa.gov.tw/index">人事行政總處全球資訊網</a></p>
      <p>2.語音查詢電話： ０２０３００１６６</p>
      <p>3.機關、學校中英文名稱係由各通報機關提供。</p>
      <p>
        4.適用範圍為各級政府機關及公、私立學校；至交通運輸、警察、消防、海岸巡防、醫療、關務等業務性質特殊機關（構），為全年無休服務民眾，且應實施輪班、輪休制度，如遇天然災害發生時，其尚無停止上班之適用。
      </p>
      <p>
        5.民間事業單位及勞工應依勞動部『天然災害發生事業單位勞工出勤管理及工資給付要點』處理， 如有疑義，請按
        <a href="https://laws.mol.gov.tw/FLAW/FLAWDAT01.aspx?id=FL049533">「勞動部網頁」</a
        >查詢，或電洽該部免付費電話專線：0800-085-151。
      </p>
    </td>
  </tr>
</tbody>
```
