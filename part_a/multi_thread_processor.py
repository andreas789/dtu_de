import multiprocessing as mp


def process_record(record):
    result = record * 2
    return result


def process_chunk(chunk):
    return [process_record(record) for record in chunk]


def main():

    records = list(range(100_000_000))

    cpu_cores = mp.cpu_count()

    chunk_size = len(records) // cpu_cores
    chunks = [records[i : i + chunk_size] for i in range(0, len(records), chunk_size)]

    with mp.Pool(processes=cpu_cores) as p:
        results = p.map(process_chunk, chunks)

    f_results = [row for sublist in results for row in sublist]

    print(f"Processed {len(f_results)} records using {cpu_cores} cores")


if __name__ == "__main__":
    main()
