require "fileutils"
require "minitest/autorun"
require "tmpdir"

require "xdrgen"
require_relative "../generator/generator"

class GeneratorSnapshotTest < Minitest::Test
  FIXTURES_DIR = File.expand_path("fixtures/xdrgen", __dir__)
  SNAPSHOTS_DIR = File.expand_path("snapshots", __dir__)
  UPDATE_SNAPSHOTS = ENV["UPDATE_SNAPSHOTS"] == "1"

  def test_fixture_snapshots
    fixtures = fixture_paths
    refute_empty fixtures, "No fixture files were found in #{FIXTURES_DIR}"

    fixtures.each do |fixture_path|
      assert_fixture_snapshot(fixture_path)
    end
  end

  private

  def fixture_paths
    Dir[File.join(FIXTURES_DIR, "*.x")].sort
  end

  def assert_fixture_snapshot(fixture_path)
    fixture_name = File.basename(fixture_path, ".x")
    snapshot_dir = File.join(SNAPSHOTS_DIR, fixture_name)

    Dir.mktmpdir("xdrgen-#{fixture_name}-") do |tmp_dir|
      generated_dir = File.join(tmp_dir, "generated")
      compile_fixture(fixture_path, generated_dir)

      if UPDATE_SNAPSHOTS
        FileUtils.rm_rf(snapshot_dir)
        FileUtils.mkdir_p(snapshot_dir)
        FileUtils.cp_r("#{generated_dir}/.", snapshot_dir)
        next
      end

      assert File.directory?(snapshot_dir), <<~MSG
        Missing snapshot for #{fixture_name}.
        Run UPDATE_SNAPSHOTS=1 bundle exec ruby test/generator_snapshot_test.rb
      MSG

      assert_files_match(snapshot_dir, generated_dir, fixture_name)
    end
  end

  def compile_fixture(fixture_path, output_dir)
    FileUtils.mkdir_p(output_dir)
    Xdrgen::Compilation.new(
      [fixture_path],
      output_dir: output_dir,
      generator: Generator,
      namespace: "stellar"
    ).compile
  end

  def assert_files_match(expected_dir, actual_dir, fixture_name)
    expected_files = collect_relative_files(expected_dir)
    actual_files = collect_relative_files(actual_dir)

    assert_equal expected_files, actual_files, <<~MSG
      Generated file list changed for fixture #{fixture_name}.
      Expected: #{expected_files.join(", ")}
      Actual:   #{actual_files.join(", ")}
    MSG

    expected_files.each do |relative_path|
      expected_path = File.join(expected_dir, relative_path)
      actual_path = File.join(actual_dir, relative_path)
      expected_content = File.binread(expected_path)
      actual_content = File.binread(actual_path)

      assert_equal expected_content, actual_content, <<~MSG
        Generated content changed for fixture #{fixture_name}: #{relative_path}
      MSG
    end
  end

  def collect_relative_files(root_dir)
    Dir.chdir(root_dir) do
      Dir.glob("**/*", File::FNM_DOTMATCH).sort.select { |path| File.file?(path) }
    end
  end
end
