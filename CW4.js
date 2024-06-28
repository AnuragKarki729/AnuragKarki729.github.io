// L = [1,2,3,4,5,6,7,8,9,10]
 
// let sum = 0
 
// for(let i=0; i<L.length; i++) {
//     sum += L[i]
// }
 
// console.log(sum)
 
// let sum2 = 0
 
// // Full form fonction
// function add(a,b) {
//     return a + b
// }
// sum2 = L.reduce(add)
 
// // Arrow (Annoymous) function
// sum2 = L.reduce((a, b) => a + b)
 
// console.log(sum2)
 
// // Find total multiplication value of the lis
// let product = 0

// product = L.reduce((a,b) => a * b)

// console.log(product)

// L = [6,7,4,10,3,8,1,9,5,2]
 
// // Sort the list in ascending order
// // for(let i=0; i<L.length; i++) {
// //     for(let j=0; j<L.length; j++) {
// //         if(L[i] < L[j]) {
// //             let temp = L[i]
// //             L[i] = L[j]
// //             L[j] = temp
// //         }
// //     }
// // }
 
// L.sort((a,b)=> a-b) //ascending
// L.sort((a,b)=> b-a) //descending
// console.log(L)

// A = ['a','b','c']
// B = ['d','e','f']
// C = A.concat(B).sort()
// console.log(C)
    L = [
        { id: 6511234, name: 'Jack', salary: 10000 },
        { id: 6511235, name: 'Mike', salary: 15000 },
        { id: 6511236, name: 'Nancy', salary: 20000 },
        { id: 6511237, name: 'Alice', salary: 30000 },
    ]
     
    var bonus = 0.2
    console.table(L)
     
    // for(let i=0; i<L.length; i++) {
    //     L[i].salary *= 1.1
    //     // console.log(L[i].salary)
    // }
     
    L.map((emp) => emp.salary *= 1.1)
     
    console.table(L)

    L.map((emp) => emp.bonus =  emp.salary * bonus)
    
    L.sort((a,b) => a.name.localeCompare(b.name))


    console.table(L)