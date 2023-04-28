use edi;
fn main() {
    let contents = std::fs::read_to_string("./scratch/edi.X12").unwrap();
    let doc = edi::parse(&contents).unwrap();
    println!("{}", doc.to_x12_string())
}
