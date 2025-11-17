fn shellsort(elems: &[i32]) -> Vec<i32> {
    let mut sorted_elems = elems.to_vec();
    let gaps = [701, 301, 132, 57, 23, 10, 4, 1];
    
    for gap in gaps {
        for i in gap..sorted_elems.len() {
            let temp = sorted_elems[i];
            let mut j = i;
            
            while j >= gap && sorted_elems[j - gap] > temp {
                sorted_elems[j] = sorted_elems[j - gap];
                j -= gap;
            }
            sorted_elems[j] = temp;
        }
    }
    
    sorted_elems
}