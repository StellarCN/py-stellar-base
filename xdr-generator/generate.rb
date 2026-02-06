require 'xdrgen'
require_relative 'generator/generator'

puts "Generating Python XDR classes..."

Dir.chdir("..")

Xdrgen::Compilation.new(
  Dir.glob("xdr/*.x"),
  output_dir: "stellar_sdk/xdr/",
  generator: Generator,
  namespace: "stellar",
).compile

puts "Done!"
