const mock = require('./mock.json')
const resjson = require('./process.json')

const all_key = Object.keys(mock)

console.log(all_key.length)

let res1 = all_key.every(key => 
  mock[key].every(key => all_key.includes(key))  
)

let res2 = resjson.every(
  reslist => {
    let a = new Set(reslist)
    return reslist.length === a.size
  }
)


let res3 = []
resjson.forEach(list => {
  res3.push(...list)
})

let res4 = res3.sort().filter((val, index) => {
  return val===res3[index+1]
})

let res5 = new Set(res3).size === all_key.filter(base => mock[base].length!==0).length

console.log(res1, res2, res3.length, res4, res5)
