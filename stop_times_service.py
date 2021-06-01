import pandas as pd
from main.dao.stop_times_dao import StopTimesDAO
from main.dao.trips_dao import TripsDAO


class StopTimesService:

    @staticmethod
    def stop_times_import_s():
        """ Service for importing csv to the db"""
        path_to_file = 'data/stop_times.txt'
        df = pd.read_csv(path_to_file, usecols=['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence'])
        df.index = [x for x in range(1, len(df.values)+1)]
        df.index.name = 'id'
        StopTimesDAO.import_dao(df=df)

        return df

    @staticmethod
    def st_import_fix_hours():
        """
        This handles the bad format of arrival_time and departure_time
        of StopTimes objects, changes wrong hour (i.e. 27:00 to 03:00)
        Saves this as datetime.time object in the db
        :return: df
        """
        path_to_file = 'data/stop_times.txt'
        df = pd.read_csv(path_to_file, usecols=['trip_id', 'arrival_time', 'departure_time', 'stop_id', 'stop_sequence'])
        df.index = [x for x in range(1, len(df.values) + 1)]
        df.index.name = 'id'
        s = df['arrival_time'].str.split(":", expand=True)
        s[0] = s[0].str.replace('24', '00')
        s[0] = s[0].str.replace('25', '01')
        s[0] = s[0].str.replace('26', '02')
        s[0] = s[0].str.replace('27', '03')
        s[0] = s[0].str.replace('28', '04')
        s[0] = s[0].str.replace('29', '05')
        s[0] = s[0].str.replace('30', '06')
        s['arrival_time'] = s[0] + ":" + s[1] + ":" + s[2]
        df['arrival_time'] = s['arrival_time']
        s = df['departure_time'].str.split(":", expand=True)
        s[0] = s[0].str.replace('24', '00')
        s[0] = s[0].str.replace('25', '01')
        s[0] = s[0].str.replace('26', '02')
        s[0] = s[0].str.replace('27', '03')
        s[0] = s[0].str.replace('28', '04')
        s[0] = s[0].str.replace('29', '05')
        s[0] = s[0].str.replace('30', '06')
        s['departure_time'] = s[0] + ":" + s[1] + ":" + s[2]
        df['departure_time'] = s['departure_time']
        df['arrival_time'] = pd.to_datetime(df['arrival_time'], format='%H:%M:%S').dt.time
        df['departure_time'] = pd.to_datetime(df['departure_time'], format= '%H:%M:%S').dt.time
        StopTimesDAO.import_dao(df=df)

        return df

    @staticmethod
    def function(start_stop, end_stop):
        fitting_trips = []
        avalaible_trips = StopTimesDAO.search_for_stop(start_stop)
        for trip in avalaible_trips:
            all_trip_stops = StopTimesDAO.get_all_stops_for_trip(trip.trip_id)
            for stop in all_trip_stops:
                if stop.stop_id == end_stop:
                    fitting_trips.append(
                        {
                            "trip_id": stop.trip_id,
                            "arrival_time": stop.arrival_time,
                            "departure_time": stop.departure_time,
                            "stop_id": stop.stop_id,
                            "stop_sequence": stop.stop_sequence
                        }
                    )
        return fitting_trips

    @staticmethod
    def function2(start_stop, end_stop):
        fitting_trips = []
        available_trips = StopTimesDAO.search_for_stop(start_stop)
        matching_trips = StopTimesDAO.search_for_stop(end_stop)
        for trip in available_trips:
            for trip2 in matching_trips:
                if trip.trip_id == trip2.trip_id:

                    fitting_trips.append(
                        {
                            "trip_id": trip.trip_id,
                            "arrival_time": str(trip.arrival_time),
                            "departure_time": str(trip.departure_time),
                            "stop_id": trip.stop_id,
                            "stop_sequence": trip.stop_sequence
                        }
                    )
        return fitting_trips

    @staticmethod
    def search_direct(start_stop, end_stop):
        """
        Searches for direct connection between start stop_id
        and end stop_id, returns all the connections possible
        :param start_stop: Int- ID of the stop that journey starts on
        :param end_stop: Int- ID of the stop that journey ends on
        :return: [{}] list of dict with trip names
        """
        fitting_trips = []
        trip_id1 = []
        trip_id2 = []
        available_trips = StopTimesDAO.search_for_stop(start_stop)
        matching_trips = StopTimesDAO.search_for_stop(end_stop)
        for row in available_trips:
            trip_id1.append(row.trip_id)
        trip_id1 = set(trip_id1)

        for row in matching_trips:
            trip_id2.append(row.trip_id)
        trip_id2 = set(trip_id2)
        for trip in trip_id1:
            for trip2 in trip_id2:
                if trip == trip2:

                    fitting_trips.append(trip)
        data = []
        # given_time = hour + ":" + minute
        # given_time = datetime.strptime(given_time, "%H:%M")
        for trip in fitting_trips:
            # arr_time = datetime.strptime(trip.arrival_time.strftime("%H:%M:%S"), "%H:%M:%S")
            # timediff = arr_time - given_time
            # seconds = timediff.total_seconds()
            # if 0 < seconds < 7200:
            trip_name = TripsDAO.get_trip_name(trip)
            data.append(
                {
                    "trip_name": trip_name,
                }
            )

        return data

    @staticmethod
    def direct_with_time(start_stop, end_stop, hour, minute):
        """
        Searches for direct connection between start stop_id
        and end stop_id, returns all the connections possible
        Searches for departures 30 mins to the future of given time

        :param start_stop: Int- ID of the stop that journey starts on
        :param end_stop: Int- ID of the stop that journey ends on
        :param hour: Hour of planning start
        :param minute: Minute of planning start
        :return: [{}] list of dict with trip names, route names and departure times
        """
        fitting_trips = []
        available_trips = StopTimesDAO.search_join_for_variants(start_stop, hour, minute, how_many_minutes=30)
        matching_trips = StopTimesDAO.search_for_stop_time(end_stop, hour, minute, how_many_minutes=60)
        available_trips = StopTimesService.search_for_unique(available_trips)
        for trip in available_trips:
            s_t_object, variant_id = trip
            for trip2 in matching_trips:
                if s_t_object.trip_id == trip2.trip_id:
                    fitting_trips.append(s_t_object)
        data = []
        for trip in fitting_trips:
            trip_name, route_name = TripsDAO.get_trip_name(trip.trip_id)
            data.append(
                {
                    "route": route_name,
                    "trip_name": trip_name,
                    "departure_time": str(trip.departure_time)
                }
            )

        return data

    @staticmethod
    def search_for_unique(res):
        unique = []
        result_unique = []
        for r in res:
            *stoptimes, variant_id = r
            if variant_id not in unique:
                unique.append(variant_id)
                result_unique.append(r)
        return result_unique

#
# def add_all_stops_to_trip():
#     trips_with_stops = []
#     i = 0
#     all_trips = create_list_of_all_trip_id()
#     all_stops = get_all()
#     for stop in all_stops:
#         for trip in all_trips:
#             i += 1
#             trips_with_stops.append(trip)
#             if stop.trip_id == trip:
#                 trips_with_stops[i].append(stop)
#
#     return trips_with_stops

