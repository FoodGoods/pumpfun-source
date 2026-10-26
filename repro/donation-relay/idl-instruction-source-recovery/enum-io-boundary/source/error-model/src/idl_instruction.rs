//! Reconstructed framework IDL instruction enum, following Anchor0.31.1.
//! Public Apache-2.0 wire API; names/layout are source, no target bytecode inputs.
use solana_program::pubkey::Pubkey;
#[derive(borsh::BorshSerialize, borsh::BorshDeserialize)]
pub enum IdlInstruction {
    Create { data_len: u64 },
    CreateBuffer,
    Write { data: Vec<u8> },
    SetBuffer,
    SetAuthority { new_authority: Pubkey },
    Close,
    Resize { data_len: u64 },
}

/// Return the native I/O result before the generated program maps its error.
pub fn deserialize_idl_instruction(buf: &mut &[u8]) -> std::io::Result<IdlInstruction> {
    <IdlInstruction as borsh::BorshDeserialize>::deserialize(buf)
}
