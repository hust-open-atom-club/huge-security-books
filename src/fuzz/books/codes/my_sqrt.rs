fn my_sqrt(x: f64) -> f64 {
    let mut approx = x / 2.0;
    let mut guess = (approx + x / approx) / 2.0;
    
    while approx != guess {
        approx = guess;
        guess = (approx + x / approx) / 2.0;
    }
    
    approx
}

fn main() {
    my_sqrt(0.0);
}
