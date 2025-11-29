import XLSX from 'xlsx';
import fs from 'fs';

// 读取Excel文件
const workbook = XLSX.readFile('123.xlsx');
const sheetName = workbook.SheetNames[0]; // 获取第一个工作表
const worksheet = workbook.Sheets[sheetName];

// 将工作表转换为JSON
const jsonData = XLSX.utils.sheet_to_json(worksheet);

// 输出JSON数据以便查看
console.log('Excel数据:');
console.log(JSON.stringify(jsonData, null, 2));

// 提取nowcoderid列的数据 - 在Excel中该列的标题为"4个平台id名字统计_9"
// 过滤掉第一行（表头说明）和最后一行（总计）
const nowcoderIds = jsonData
  .slice(1) // 跳过第一行（表头说明）
  .map(row => row["4个平台id名字统计_9"] || undefined)
  .slice(0, -1); // 移除最后一行（总计）

console.log('\nNowcoder IDs:');
console.log(nowcoderIds);

// 读取user.json文件
const userJson = JSON.parse(fs.readFileSync('user.json', 'utf8'));

console.log('\n当前user.json中的用户数量:', userJson.length);
console.log('Excel中用户数量:', jsonData.length);

// 将nowcoderid添加到user.json中
const updatedUserJson = userJson.map((user, index) => {
    if (index < nowcoderIds.length && nowcoderIds[index]) {
        return {
            ...user,
            nowcoder_id: nowcoderIds[index]
        };
    }
    return user;
});

// 写回更新后的user.json
fs.writeFileSync('user.json', JSON.stringify(updatedUserJson, null, 2));
console.log('\n已将nowcoderid添加到user.json中');