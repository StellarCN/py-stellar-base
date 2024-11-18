#![no_std]
use soroban_sdk::{
    contract, contracterror, contractimpl, contracttype, symbol_short, vec, Address, Bytes, BytesN,
    Env, Map, String, Symbol, Val, Vec, I256, U256,
};

#[contract]
pub struct Contract;

/// This is from the rust doc above the struct Test
#[contracttype]
pub struct Test {
    pub a: u32,
    pub b: bool,
    pub c: Symbol,
}

#[contracttype]
pub enum SimpleEnum {
    First,
    Second,
    Third,
}

#[contracttype]
#[derive(Clone, Copy)]
// The `repr` attribute is here to specify the memory alignment for this type
#[repr(u32)]
pub enum RoyalCard {
    // TODO: create the fields here for your `RoyalCard` type
    Jack = 11,  // delete this
    Queen = 12, // delete this
    King = 13,  // delete this
}

#[contracttype]
pub struct TupleStruct(Test, SimpleEnum);

#[contracttype]
pub enum ComplexEnum {
    Struct(Test),
    Tuple(TupleStruct),
    Enum(SimpleEnum),
    Asset(Address, i128),
    Void,
}

#[contracterror]
#[derive(Copy, Clone, Debug, Eq, PartialEq, PartialOrd, Ord)]
#[repr(u32)]
pub enum Error {
    /// Please provide an odd number
    NumberMustBeOdd = 1,
}
#[contractimpl]
impl Contract {
    pub fn hello(_env: Env, hello: Symbol) -> Symbol {
        hello
    }

    pub fn woid(_env: Env) {
        // do nothing
    }

    pub fn val(_env: Env) -> Val {
        Val::default()
    }

    pub fn u32_fail_on_even(_env: Env, u32_: u32) -> Result<u32, Error> {
        if u32_ % 2 == 1 {
            Ok(u32_)
        } else {
            Err(Error::NumberMustBeOdd)
        }
    }

    pub fn u32_(_env: Env, u32_: u32) -> u32 {
        u32_
    }

    pub fn i32_(_env: Env, i32_: i32) -> i32 {
        i32_
    }

    pub fn i64_(_env: Env, i64_: i64) -> i64 {
        i64_
    }

    /// Example contract method which takes a struct
    pub fn strukt_hel(env: Env, strukt: Test) -> Vec<Symbol> {
        vec![&env, symbol_short!("Hello"), strukt.c]
    }

    pub fn strukt(_env: Env, strukt: Test) -> Test {
        strukt
    }

    pub fn simple(_env: Env, simple: SimpleEnum) -> SimpleEnum {
        simple
    }

    pub fn complex(_env: Env, complex: ComplexEnum) -> ComplexEnum {
        complex
    }

    pub fn addresse(_env: Env, addresse: Address) -> Address {
        addresse
    }

    pub fn bytes(_env: Env, bytes: Bytes) -> Bytes {
        bytes
    }

    pub fn bytes_n(_env: Env, bytes_n: BytesN<9>) -> BytesN<9> {
        bytes_n
    }

    pub fn card(_env: Env, card: RoyalCard) -> RoyalCard {
        card
    }

    pub fn boolean(_: Env, boolean: bool) -> bool {
        boolean
    }

    /// Negates a boolean value
    pub fn not(_env: Env, boolean: bool) -> bool {
        !boolean
    }

    pub fn i128(_env: Env, i128: i128) -> i128 {
        i128
    }

    pub fn u128(_env: Env, u128: u128) -> u128 {
        u128
    }

    pub fn multi_args(_env: Env, a: u32, b: bool) -> u32 {
        if b {
            a
        } else {
            0
        }
    }

    pub fn map(_env: Env, map: Map<u32, bool>) -> Map<u32, bool> {
        map
    }

    pub fn vec(_env: Env, vec: Vec<u32>) -> Vec<u32> {
        vec
    }

    pub fn tuple(_env: Env, tuple: (Symbol, u32)) -> (Symbol, u32) {
        tuple
    }

    /// Example of an optional argument
    pub fn option(_env: Env, option: Option<u32>) -> Option<u32> {
        option
    }

    pub fn u256(_env: Env, u256: U256) -> U256 {
        u256
    }

    pub fn i256(_env: Env, i256: I256) -> I256 {
        i256
    }

    pub fn string(_env: Env, string: String) -> String {
        string
    }

    pub fn tuple_strukt(_env: Env, tuple_strukt: TupleStruct) -> TupleStruct {
        tuple_strukt
    }

    // pub fn timepoint(_env: Env, timepoint: TimePoint) -> TimePoint {
    //     timepoint
    // }

    // pub fn duration(_env: Env, duration: Duration) -> Duration {
    //     duration
    // }
}
